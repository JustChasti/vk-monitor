from time import sleep

from pymongo import MongoClient
from loguru import logger

from config import base_domen, base_port, client_name, default_collection_name
from config import photos_collection

while True:
    try:
        client = MongoClient(
            host=base_domen,
            port=base_port,
        )
        db = client[client_name]
        collection = db[default_collection_name]
        photoscoll = db[photos_collection]
        break
    except Exception as e:
        logger.exception(e)
        sleep(5)
