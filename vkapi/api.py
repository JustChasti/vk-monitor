import requests
import json
import time
import urllib.request
import os

from loguru import logger

from config import token
from config import max_photo_save
from src.db import collection, jobs_collection


class ConnectionError(Exception):
    pass


class NoResultsError(Exception):
    pass


save_photo_counter = 0


def get_photos(job, start_time, end_time, count, offset):
    q = job['q']
    lat = job['lat']
    longg = job['longg']
    radius = job['radius']
    url = (f'https://api.vk.com/method/photos.search?'
           f'&access_token={token}&v=5.131&'
           f'q={q}&lat={lat}&long={longg}&offset={offset}&start_time={start_time}&'
           f'end_time={end_time}&count={count}&radius={radius}&sort=0')
    response = requests.get(url)
    if response.status_code != 200:
        raise ConnectionError("I can't connect to server")
    try:
        data = response.json()["error"]
        logger.warning("We off the limit")
        if int(data["error_code"]) == 6:
            time.sleep(1)
            get_photos(job, start_time, end_time, count, offset)
        else:
            logger.error("Invalid request")
            raise ConnectionError("Invalid request")
    except Exception as e:
        data = response.json()["response"]
        items = data["items"]
        for i in items:
            element = {}
            element["album_id"] = i["album_id"]
            element["date"] = i["date"]
            element["id"] = i["id"]
            element["owner_id"] = i["owner_id"]
            if i["text"]:
                element["text"] = i["text"]
            element["has_tags"] = i["has_tags"]
            element["photo"] = i["sizes"][-1]["url"]
            add_photo(element)
        if count + offset < data["count"]:
            offset += count
            get_photos(job, start_time, end_time, count, offset)


def add_photo(element):
    result = collection.find_one({'id': element["id"]})
    if result:
        logger.warning('Duplicate photo')
    else:
        collection.insert_one(element)
        global save_photo_counter
        save_photo_counter += 1
        if max_photo_save != 0:
            if save_photo_counter <= max_photo_save:
                os.mkdir(f'data/{element["id"]}')
                try:
                    urllib.request.urlretrieve(element["photo"],
                                               f'data/{element["id"]}/{element["id"]}.jpg')
                except Exception as e:
                    logger.warning("Cant save this photo")
        else:
            os.mkdir(f'data/{element["id"]}')
            try:
                urllib.request.urlretrieve(element["photo"],
                                           f'data/{element["id"]}/{element["id"]}.jpg')
            except Exception as e:
                logger.warning("Cant save this photo")


def distributor(job, start_time, end_time, count):
    q = job['q']
    lat = job['lat']
    longg = job['longg']
    radius = job['radius']
    url = (f'https://api.vk.com/method/photos.search?'
           f'&access_token={token}&v=5.131&'
           f'q={q}&lat={lat}&long={longg}&start_time={start_time}&'
           f'end_time={end_time}&count={count}&radius={radius}&sort=0')
    response = requests.get(url)
    if response.status_code != 200:
        raise ConnectionError("I can't connect to server")
    try:
        data = response.json()["error"]
        if int(data["error_code"]) == 6:
            time.sleep(1)
            distributor(job, start_time, end_time, count)
        else:
            raise ConnectionError("Invalid request")
    except Exception as e:
        data = response.json()["response"]
        quantity = int(data["count"])
        if quantity == 0:
            raise NoResultsError("NO results")
        print(quantity)
        if quantity > 3000:
            middle_time = (start_time + end_time)/2
            distributor(job, start_time, middle_time, count)
            distributor(job, middle_time, end_time, count)
        else:
            get_photos(job, start_time, end_time, 10, 0)


if __name__ == "__main__":
    while True:
        try:
            job = jobs_collection.find_one({'Success': False})
            if job:
                distributor(job, job['begin_time'], time.time(), 10)
                logger.info("job complete")
                jobs_collection.update_one({'_id': job['_id']},
                                           {"$set": {'Success': True}})
            else:
                logger.info("Theres no new jobs")
        except Exception as e:
            logger.exception(e)
        time.sleep(10)
