import json

from flask import Flask, request, jsonify
from loguru import logger

from src.db import collection


application = Flask(__name__)


@application.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


@application.route("/jobs/send_new", methods=["POST"])
def send_job():
    response = request.get_json(force=True)
    response['Success'] = False
    result = collection.find_one({'name': response["name"]})
    if result:
        logger.warning("Duplicate joba")
        return json.dumps({'info': 'job name must be unic'}), 201, {'ContentType': 'application/json'}
    else:
        print(response)
        collection.insert_one(response)
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == "__main__":
    application.run()
