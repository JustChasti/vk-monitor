from time import sleep

from pymongo import MongoClient
from loguru import logger

from config import base_domen, base_port, client_name, default_collection_name, jobs_collection_name

while True:
    try:
        client = MongoClient(
            host=base_domen,
            port=base_port,
        )
        db = client[client_name]
        collection = db[default_collection_name]
        jobs_collection = db[jobs_collection_name]
        break
    except Exception as e:
        logger.exception(e)
        sleep(5)
