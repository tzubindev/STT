import requests
import json

url = "http://127.0.0.1:8000/stt/audio"
data = {"url": "testing"}


response = requests.post(url, json=data)
# print(response.json())

with open("./result/r1.json", "w") as f:
    json.dump(response.json(), f, ensure_ascii=False, indent=4)

import webbrowser
import os

response = None

with open("./result/r1.json", "r") as f1:
    response = dict(json.loads("".join(f1.readlines())))

with open("./output/test.html", "w") as f:
    f.write(response["sensitive_words"]["html"])

# to get the current working directory
directory = os.getcwd()
webbrowser.open(directory + "/output/test.html")
