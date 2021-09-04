import requests
import json


def send():
    data = {
        "name": "Test5",
        "q": "Футбол",
        "lat": 55.755865,
        "longg": 37.617520,
        "begin_time": 1420074061,
        "radius": 10000
        }
    answer = requests.post('http://127.0.0.1:5000/'+'jobs/send_new',
                           verify=False, data=json.dumps(data))
    print(answer)


send()
