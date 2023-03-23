import requests
import json


url = "http://127.0.0.1:8000/stt/updateSender/1/ClientA_AgentA_22-03-2023_1"
data = {"sender": "client", "old_sender": "agent"}
headers = {"Content-Type": "application/json", "Authorization": "asdasd8adasd"}


response = requests.post(url, json=data, headers=headers)
print(response.json())

with open("./result/r1.json", "w") as f:
    json.dump(response.json(), f, ensure_ascii=False, indent=4)

# import webbrowser
# import os

# response = None

# with open("./result/r1.json", "r") as f1:
#     response = dict(json.loads("".join(f1.readlines())))

# with open("./output/test.html", "w") as f:
#     f.write(response["sensitive_words"]["html"])

# # to get the current working directory
# directory = os.getcwd()
# webbrowser.open(directory + "/output/test.html")

# url = "http://127.0.0.1:8000/stt/text"
# textData = {"string": "very long text asdsadasdsasadds"}
# try:
#     response = requests.post(url, data=json.dumps(textData))
#     print("Response body:", response.json())
# except requests.exceptions.RequestException as e:
#     print("Error:", e)


# Test Update comment Database
# request_id = "client_agent_20-02-2023_1"
# conversation_id = 1
# data = {"comment": "Test"}
# response = requests.post(f"http://127.0.0.1:8000/stt/updateComment/{conversation_id}/{request_id}", json=data)
# print(response.json())

# Test Update sender Database
# request_id = "Byng_Ghassan_22-02-2023_1"
# conversation_id = 1
# data = {"sender": "Agent"}
# response = requests.post(f"http://127.0.0.1:8000/stt/updateSender/{conversation_id}/{request_id}", json=data)
# print(response.json())

# Test Get data for org
# org_id = "org1"
# response = requests.get(f"http://127.0.0.1:8000/stt/requests/{org_id}")
# response_text = response.text.replace('\\', '')
# print(response_text)

# Test Get data for req
# req_id = "Byng_Ghassan_22-02-2023_1"
# url = f"http://127.0.0.1:8000/stt/request/{req_id}"
# response = requests.get(url)
# print(response.json())

# Test Delete Database
# url = "http://127.0.0.1:8000/stt/database"
# data = {"Request_ID": "Byng_Ghassan_22-02-2023_1"}
# response = requests.delete(url, json=data)
# print(response.text)
