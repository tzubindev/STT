import requests


url = "https://stt-api.tamade.dev/stt/audio"
body = {"url": "testing"}


response = requests.post(url, json=body)
print(response.json())
