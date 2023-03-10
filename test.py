import requests
import json

url = "http://127.0.0.1:8000/stt/audio"
data = {"url": "testing"}


response = requests.post(url, json=data)
# print(response.json())

with open("./result/r1.json", "w") as f:
    json.dump(response.json(), f, ensure_ascii=False, indent=4)

import requests

url = "http://127.0.0.1:8000/stt/audio"
data = {"url": "PUT YOUR AUDIO URL HERE"}
response = requests.post(url, json=data)
