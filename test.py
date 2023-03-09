import requests


url = "http://127.0.0.1:8000/stt/audio"
body = {"url": "testing"}


response = requests.post(url, json=body)
print(response.json())
