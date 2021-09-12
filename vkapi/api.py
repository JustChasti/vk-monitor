from logging import info
import requests
import time
import urllib.request
import os
import sys

from loguru import logger
from requests.api import get

from config import token
from src.db import collection, jobs_collection


class ConnectionError(Exception):
    pass


class NoResultsError(Exception):
    pass


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

    except ConnectionError as e:
        logger.exception(e)
    except Exception as e:
        pass

    try:
        data = response.json()["response"]
        items = data["items"]
        for i in items:
            add_photo({
                "job_name": job['name'],
                "album_id": i["album_id"],
                "date": i["date"],
                "id": i["id"],
                "owner_id": i["owner_id"],
                "text": i.get("text", ""),
                "has_tags": i["has_tags"],
                "photo": i["sizes"][-1]["url"]
            })
        if count + offset < data["count"]:
            offset += count
            get_photos(job, start_time, end_time, count, offset)
        else:
            return None
    except Exception as e:
        logger.warning("This request to api fall")
        logger.warning(response.json())


def add_photo(element):
    result = collection.find_one({'id': element["id"]})
    if result:
        logger.warning('Duplicate photo')
    else:
        collection.insert_one(element)
        try:
            os.mkdir(f'data/{element["id"]}')
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

    except ConnectionError as e:
        logger.exception(e)
    except Exception as e:
        pass

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


def starter(job, begin_time, now_time):
    jobs_collection.update_one(
        {'_id': job['_id']},
        {"$set": {'active': True}}
    )
    try:
        distributor(job, begin_time, now_time, 10)
        logger.info("job complete")
        jobs_collection.update_one(
            {'_id': job['_id']},
            {"$set": {'Success': True, 'active': False}}
        )
    except NoResultsError:
        logger.info(f"No results for {job['name']}")
        jobs_collection.update_one(
            {'_id': job['_id']},
            {"$set": {'Success': True, 'active': False}}
        )
    except Exception as e:
        logger.exception(e)
        jobs_collection.update_one(
            {'_id': job['_id']},
            {"$set": {'active': False}}
        )


if __name__ == "__main__":
    jobs_collection.update_many(
        {'Success': False},
        {"$set": {'active': False}}
    )
    sys.setrecursionlimit(1000000)
    try:
        os.mkdir('data')
    except FileExistsError as e:
        pass
    try:
        logger.add("vkphoto.log")
    except FileExistsError as e:
        pass
    while True:
        try:
            job = jobs_collection.find_one({'Success': False, 'active': False})
            if job:
                starter(job, job['begin_time'], time.time())
            else:
                logger.info("Theres no active jobs")
        except Exception as e:
            logger.exception(e)
        time.sleep(5)
