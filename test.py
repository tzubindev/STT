import requests
import json

url = "http://127.0.0.1:8000/stt/audio"
data = {
    "url": "https://microtel-devops-3oagotijeofb69fts7hnges51j5oeaps1a-s3alias.s3.ap-southeast-1.amazonaws.com/uatrecordings/ba2b80d2-089f-46db-b6d9-e2dd70aa2ac8/5576ee39-4073-443d-bbfa-441a02bc3854/2023/2/8/c1da7a87-85c8-485d-828b-804d47b65b4b.mp3?AWSAccessKeyId=AKIA4RSNX3RTDVIKBQEP&Expires=1678265727&Signature=hMONxgw9BEWXfTZKj3WDIy4qw6M%3D"
}


response = requests.post(url, json=data)
# print(response.json())

with open("./result/r1.json", "w") as f:
    json.dump(response.json(), f, ensure_ascii=False, indent=4)
