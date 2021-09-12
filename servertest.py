import requests
import json
from loguru import logger


def send():
    data = {
        "name": "Test2",
        "q": "Футбол",
        "lat": 55.755865,
        "long": 37.617520,
        "begin_time": 1420074061,
        "radius": 10000
        }
    data = {
        "name": "Test4",
        "q": "Петербург",
        "lat": 59.938942,
        "long": 30.315742,
        "begin_time": 1420074061,
        "radius": 10000
        }
    answer = requests.post('http://45.90.35.48/'+'jobs/send_new',
                           verify=False, data=json.dumps(data))
    print(answer)


send()
# answer = requests.get('http://127.0.0.1:5000/'+'jobs/all')
# print(answer)

