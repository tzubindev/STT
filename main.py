from text_processing import TextProcessing
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sensitive_words_marking import SensitiveWordsMarking
from transcribe import Transcribe
from naivebayes import NaiveBayes
from textblob import TextBlob
import pyodbc as odcb
import json
import collections
from fastapi import Body
from dotenv import dotenv_values
import os
import itertools

config = dotenv_values(".env")
connection_string = f"DRIVER={{SQL Server}};SERVER={config['SERVER']};DATABASE={config['DATABASE']};UID={config['USERNAME']};PWD={config['PASSWORD']}"

# Create the connection to SQL SERVER
conn = odcb.connect(connection_string)

cursor = conn.cursor()


class AudioQuery(BaseModel):
    url: str
    client_name: str
    agent_name: str
    date: str
    unique_number: int


class TextQuery(BaseModel):
    string: str


class CommentQuery(BaseModel):
    comment: str = Body(...)
    old_comment: str = Body(...)


class SenderQuery(BaseModel):
    sender: str = Body(...)
    old_sender: str = Body(...)


# class RequestUpdate(BaseModel):
#     highest_Count: int = Body(...)


class RequestDelete(BaseModel):
    Request_ID: int = Body(...)


classifier = NaiveBayes()

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    lines = None
    with open("./docs/index.html", "r", encoding="utf-8") as f:
        lines = "".join(f.readlines())
    return HTMLResponse(content=lines)


@app.get("/doc")
def Doc():
    lines = None
    with open("./docs/doc.html", "r", encoding="utf-8") as f:
        lines = "".join(f.readlines())
    return HTMLResponse(content=lines)


# @app.post("/stt/text")
# def PostText(query: TextQuery):
#     return {"response": query.string}


@app.post("/stt/addRequest/{org_id}")
def AddRequest(org_id: str, query: AudioQuery):

    result = None

    if query.url == "testing":
        # return {"Result": "Not Applicable."}
        result = Transcribe(os.getcwd() + "\\test.mp3", True).getResult()
    else:
        result = Transcribe(query.url.strip()).getResult()

    if type(result) != list:
        return {"response": "Error"}

    # Result [0] = sender
    # Result [1] = text
    conversations = []
    word_counts_sentence = ""
    cnt = 1
    request = dict()
    request[
        "Request_ID"
    ] = f"{query.client_name}_{query.agent_name}_{query.date}_{query.unique_number}"

    for r in result:
        obj = {"Conversation_ID": cnt, "Sender": r[0], "Content": r[1]}
        classifiedObj = classifier.classifySentences(r[1])
        obj["Sentiment"] = classifiedObj["sentiment"]
        obj["Confidence"] = classifiedObj["confidence"] * 100
        obj["Comment"] = ""
        obj["Request_ID"] = request["Request_ID"]
        conversations.append(obj)
        cnt += 1

        word_counts_sentence += TextProcessing(r[1]).getProcessedSentence() + " "

    word_counts = TextProcessing(word_counts_sentence).getWordCounts()
    word_counts = dict(sorted(word_counts.items(), key=lambda x: x[1], reverse=True))
    for key, value in word_counts.items():
        request["Highest_Count"] = value
        break

    request["Audio_URL"] = query.url
    request["Date"] = query.date
    request["Org_ID"] = org_id

    objCnt = 0
    posCnt = 0
    for c in conversations:
        posCnt += c["Sentiment"] == "Positive"
        objCnt += 1

    request["Sentiment_Distribution_Pos"] = posCnt / objCnt * 100
    request["Sentiment_Distribution_Neg"] = (objCnt - posCnt) / objCnt * 100

    words = []
    cnt = 1
    for key, value in word_counts.items():
        obj = dict()
        obj["Word_ID"] = cnt
        obj["Word"] = key
        obj["IsSensitive"] = SensitiveWordsMarking(key).hasSensitiveWord()
        obj["Word_Count"] = value
        obj["Request_ID"] = request["Request_ID"]
        words.append(obj)

        cnt += 1

    # final_result = [
    #     request,
    #     conversations,
    #     words,
    # ]

    # Insert Data to MSSQL
    request_list = []
    word_list = []
    conversation_list = []
  

    reuqest_insert_record = """INSERT INTO Request
                        (Request_ID, Audio_URL, Sentiment_Distribution_Pos,
                        Sentiment_Distribution_Neg, Highest_Count, Date, Org_ID)
                        VALUES (?,?,?,?,?,?,?)"""
    word_insert_record = """INSERT INTO Words
                        (Word_ID, Word, IsSensitive,
                        Word_Count, Request_ID)
                        VALUES (?,?,?,?,?)"""
    conversation_insert_record = """INSERT INTO Conversations
                        (Conversation_ID, Sender, Content,
                        Sentiment, Confidence, Comment, Request_ID)
                        VALUES (?,?,?,?,?,?,?)"""
    
    request_data = [request["Request_ID"], request["Audio_URL"], request["Sentiment_Distribution_Pos"], request["Sentiment_Distribution_Neg"], request["Highest_Count"], request["Date"], request["Org_ID"]]
    request_list.append(request_data)
    cursor.executemany(reuqest_insert_record, request_list)

    for w in words:
        words_data = [w["Word_ID"], w["Word"], w["IsSensitive"], w["Word_Count"], w["Request_ID"]]
        word_list.append(words_data)
    cursor.executemany(word_insert_record, word_list)

    for c in conversations:
        conversation_data = [c["Conversation_ID"], c["Sender"], c["Content"], c["Sentiment"], c["Confidence"], c["Comment"], c["Request_ID"] ]
        conversation_list.append(conversation_data)
    cursor.executemany(conversation_insert_record, conversation_list)
    
    conn.commit()
    return {"response": "Success"}


@app.delete("/stt/delete")
async def DeleteData(request_delete: RequestDelete):

    conn.autocommit = False
    cursor = conn.cursor()

    delete_query = """DELETE FROM Request WHERE Request_ID=?"""

    value = request_delete.Request_ID

    cursor.execute(delete_query, value)

    conn.commit()

    return {"message": "Data deleted successfully."}


@app.post("/stt/updateComment/{conversation_id}/{request_id}")
def updateComment(conversation_id: int, request_id: str, comment_update: CommentQuery):
    cursor = conn.cursor()

    select_query = """SELECT Comment FROM Conversations WHERE Request_ID= ? AND Conversation_ID=? """

    values = (request_id, conversation_id)

    cursor.execute(select_query, values)

    db_old_comment = cursor.fetchone()[0]
    if comment_update.old_comment != db_old_comment:
        conn.commit()
        return {"response": "Error"}

    update_query = """UPDATE Conversations SET Comment = ? WHERE Request_ID= ? AND Conversation_ID=? """

    values = (comment_update.comment, request_id, conversation_id)

    cursor.execute(update_query, values)

    conn.commit()

    return {"response": "Success"}


@app.post("/stt/updateSender/{conversation_id}/{request_id}")
def updateSender(conversation_id: int, request_id: str, sender_update: SenderQuery):
    cursor = conn.cursor()

    select_query = """SELECT Sender FROM Conversations WHERE Request_ID= ? AND Conversation_ID=? """

    values = (request_id, conversation_id)

    cursor.execute(select_query, values)

    db_old_sender = cursor.fetchone()[0]
    if sender_update.old_sender != db_old_sender:
        conn.commit()
        return {"response": "Error"}

    update_query = """UPDATE Conversations SET Sender = ? WHERE Request_ID= ? AND Conversation_ID=? """

    values = (sender_update.sender, request_id, conversation_id)

    cursor.execute(update_query, values)

    conn.commit()

    return {"response": "Updated Successfully"}


@app.get("/stt/requests/{org_id}")
async def ReturnRequests(org_id: str):
    cursor = conn.cursor()

    cursor.execute("SELECT Request_ID FROM Request WHERE Org_ID = ? ", org_id)
    rows = cursor.fetchall()
    RequestList = []
    for row in rows:
        data = row[0]
        RequestList.append(data)

    result = json.dumps(RequestList)

    return {"Request": result}


@app.get("/stt/request/{req_id}")
async def STT_Test(req_id: str):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Request WHERE Request_ID = ? ", req_id)
    rows = cursor.fetchall()

    for row in rows:
        data = {
            "request_id": row[0],
            "sentiment": {"distribution": {"pos": row[2], "neg": row[3]}},
            "highest_count": row[4],
            "date": row[5],
        }

    cursor.execute("SELECT * FROM Words WHERE Request_ID = ? ", req_id)
    rows = cursor.fetchall()
    objects_list = []
    for row in rows:
        object_dict = {
            "word_id": row[0],
            "word": row[1],
            "isClicked": False,
            "isSearched": True,
            "isSensitive": row[2],
            "count": row[3],
        }
        objects_list.append(object_dict)

    cursor.execute("SELECT * FROM Conversations WHERE Request_ID = ? ", req_id)
    rows = cursor.fetchall()
    objects_list1 = []
    for row in rows:
        object_dict = {
            "conversation_id": row[0],
            "from": row[1],
            "content": row[2],
            "sentiment": row[3],
            "confidence": row[4],
            "isClicked": False,
            "comment": row[5],
        }
        objects_list1.append(object_dict)

    result_dict = {
        "request_id": data["request_id"],
        "sentiment": data["sentiment"],
        "highest_count": data["highest_count"],
        "date": data["date"],
        "words": objects_list,
        "conversations": objects_list1,
    }

    result = json.dumps(result_dict)

    # with open("sample.json", "w") as outfile:
    #     outfile.write(result)

    return {"Request": result}
