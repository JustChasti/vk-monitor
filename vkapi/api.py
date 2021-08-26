import requests
import json
import time
import urllib.request
import os

from loguru import logger

from config import token, lat, q, longg, begin_time, radius
from config import max_photo_save
from src.db import collection


class ConnectionError(Exception):
    pass


class NoResultsError(Exception):
    pass


save_photo_counter = 0


def get_photos(start_time, end_time, count, offset):
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
            get_photos(start_time, end_time, count, offset)
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
            get_photos(start_time, end_time, count, offset)


def add_photo(element):
    result = collection.find_one({'id': element["id"]})
    if result:
        logger.warning('Duplicate photo')
    else:
        collection.insert_one(element)
        global save_photo_counter
        save_photo_counter += 1
        if save_photo_counter <= max_photo_save:
            os.mkdir(f'data/{element["id"]}')
            urllib.request.urlretrieve(element["photo"],
                                       f'data/{element["id"]}/{element["id"]}.jpg')


def distributor(start_time, end_time, count):
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
            distributor(start_time, end_time, count)
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
            distributor(start_time, middle_time, count)
            distributor(middle_time, end_time, count)
        else:
            get_photos(start_time, end_time, 10, 0)


if __name__ == "__main__":
    try:
        distributor(begin_time, time.time(), 10)
    except Exception as e:
        logger.exception(e)
