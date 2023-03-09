import requests


url = "http://193.168.10.212:8000/stt/audio"
body = {"url": "testing"}


response = requests.post(url, json=body)
print(response.json())
