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


@app.post("/stt/audio")
def STT_Audio(query: AudioQuery):
    result = None
    sorted_word_counts = None
    MarkedWords = None

    if query.url == "testing":
        # return {"Result": "Not Applicable."}
        result = Transcribe(os.getcwd() + "\\test.mp3", True).getText()
    else:
        result = Transcribe(query.url.strip()).getText()

    processed_result = TextProcessing(result)

    word_counts = processed_result.getWordCounts()

    sorted_word_counts = dict(
        sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    )
    sorted_word_counts = dict(itertools.islice(sorted_word_counts.items(), 5))

    markedObj = SensitiveWordsMarking(processed_result.getProcessedSentence())

    MarkedWords = dict()
    MarkedWords["has_sensitive_word"] = markedObj.hasSensitiveWord()
    MarkedWords["obj"] = markedObj.getMarkedObj()
    MarkedWords["html"] = markedObj.getMarkedHTML()

    sentiment = classifier.classifySentences(result)

    # if NaiveBayes().classifySentences(result) == 1:
    #     sentiment = "Positive"
    # else:
    #     sentiment = "Negative"

    return {
        "id": 1,
        "text": result,
        "most_frequent_words": sorted_word_counts,
        "sensitive_words": {
            "has_senstive_word": MarkedWords["has_sensitive_word"],
            "obj": MarkedWords["obj"],
            "html": MarkedWords["html"],
        },
        "sentiment": sentiment,
    }


# @app.post("/stt/text")
# def PostText(query: TextQuery):
#     return {"response": query.string}

@app.post("/stt/database")
def Test(query: AudioQuery):
    
    result = None
    sorted_word_counts = None
    MarkedWords = None

    if query.url == "testing":
        # return {"Result": "Not Applicable."}
        result = Transcribe(os.getcwd() + "\\test.mp3", True).getText()
    else:
        result = Transcribe(query.url.strip()).getText()

    processed_result = TextProcessing(result)

    word_counts = processed_result.getWordCounts()

    sorted_word_counts = dict(
        sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    )
    sorted_word_counts = dict(itertools.islice(sorted_word_counts.items(), 5))

    markedObj = SensitiveWordsMarking(processed_result.getProcessedSentence())

    MarkedWords = dict()
    MarkedWords["has_sensitive_word"] = markedObj.hasSensitiveWord()
    MarkedWords["obj"] = markedObj.getMarkedObj()
    MarkedWords["html"] = markedObj.getMarkedHTML()

    sentiment = classifier.classifySentences(result)

    request_Record_list = []
    request_Record_1 = ["", query.url, sentiment["Positive"], sentiment["Negative"], 3, "22-01-2023"]
    request_Record_list.append(request_Record_1)
    reuqest_insert_records = '''INSERT INTO Request 
                        (Request_ID, Audio_URL, Sentiment_Distribution_Pos, 
                        Sentiment_Distribution_Neg, highest_Count, Date) 
                        VALUES (?,?,?,?,?,?)''' 
    cursor.executemany(reuqest_insert_records, request_Record_list )
    conn.commit()
    return {"response": query.url}


    
@app.delete("/stt/delete")
async def DeleteData(request_delete: RequestDelete):

        conn.autocommit = False
        cursor = conn.cursor()

        delete_query = """DELETE FROM Request WHERE Request_ID=?"""
    
        value = (request_delete.Request_ID)

        cursor.execute(delete_query, value)

        conn.commit()

        return {"message": "Data deleted successfully."}

@app.post("/stt/updateComment/{conversation_id}/{request_id}")
def updateComment(conversation_id: int, request_id: str, comment_update: CommentQuery):
    cursor = conn.cursor()

    select_query = '''SELECT Comment FROM Conversations WHERE Request_ID= ? AND Conversation_ID=? '''

    values = (request_id, conversation_id)

    cursor.execute(select_query, values)

    db_old_comment = cursor.fetchone()[0]
    if comment_update.old_comment != db_old_comment:
        conn.commit()
        return {"response": "Error"}
    

    update_query = '''UPDATE Conversations SET Comment = ? WHERE Request_ID= ? AND Conversation_ID=? '''

    values = (comment_update.comment, request_id, conversation_id)

    cursor.execute(update_query, values)

    conn.commit()

    return {"response": "Success"}

@app.post("/stt/updateSender/{conversation_id}/{request_id}")
def updateSender(conversation_id: int, request_id: str, sender_update: SenderQuery):
    cursor = conn.cursor()

    select_query = '''SELECT Sender FROM Conversations WHERE Request_ID= ? AND Conversation_ID=? '''

    values = (request_id, conversation_id)

    cursor.execute(select_query, values)

    db_old_sender = cursor.fetchone()[0]
    if sender_update.old_sender != db_old_sender:
        conn.commit()
        return {"response": "Error"}
    
    update_query = '''UPDATE Conversations SET Sender = ? WHERE Request_ID= ? AND Conversation_ID=? '''

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
        data = (row[0])
        RequestList.append(data)

    result = json.dumps(RequestList)
   
    return {"Request": result}

@app.get("/stt/request/{req_id}")
async def STT_Test(req_id: str):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Request WHERE Request_ID = ? ", req_id)
    rows = cursor.fetchall()
   
    for row in rows:
        data = {'request_id': row[0], 'sentiment': {'distribution':{'pos':row[2], 'neg':row[3]}}, 'highest_count': row[4], 'date': row[5]}


    cursor.execute("SELECT * FROM Words WHERE Request_ID = ? ", req_id)
    rows = cursor.fetchall()
    objects_list = []
    for row in rows:
        object_dict = {'word_id': row[0], 'word': row[1], 'isClicked': False, 'isSearched': True, 'isSensitive': row[2], 'count': row[3]}
        objects_list.append(object_dict)

    cursor.execute("SELECT * FROM Conversations WHERE Request_ID = ? ", req_id)
    rows = cursor.fetchall()
    objects_list1 = []
    for row in rows:
        object_dict = {'conversation_id': row[0], 'from': row[1], 'content': row[2], 'sentiment': row[3], 'confidence': row[4], 'isClicked': False,'comment': row[5]}
        objects_list1.append(object_dict)

    result_dict = {
    "request_id": data['request_id'],
    "sentiment": data['sentiment'],
    "highest_count": data['highest_count'],
    "date": data['date'],
    "words": objects_list,
    "conversations": objects_list1
    }

    result = json.dumps(result_dict)

    # with open("sample.json", "w") as outfile:
    #     outfile.write(result)

    return {"Request": result}


 
