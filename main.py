from text_processing import TextProcessing
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sensitive_words_marking import SensitiveWordsMarking
from transcribe import Transcribe
from naivebayes import NaiveBayes
from textblob import TextBlob

import os
import itertools


class AudioQuery(BaseModel):
    url: str


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


@app.get("/stt/test")
def STT_Test():
    return {
        "sentiment": {
            "distribution": {
                "isPosClicked": False,
                "isNegClicked": False,
                "pos": 10,
                "neg": 90,
            }
        },
        "highest_count": 10,
        "words": [
            {
                "word": "help",
                "isClicked": False,
                "isSearched": True,
                "isSensitive": False,
                "count": 3,
            },
            {
                "word": "package",
                "isClicked": False,
                "isSearched": True,
                "isSensitive": False,
                "count": 2,
            },
            {
                "word": "Happy",
                "isClicked": False,
                "isSearched": True,
                "isSensitive": False,
                "count": 2,
            },
            {
                "word": "hello",
                "isClicked": False,
                "isSearched": True,
                "isSensitive": False,
                "count": 1,
            },
            {
                "word": "check",
                "isClicked": False,
                "isSearched": True,
                "isSensitive": False,
                "count": 1,
            },
            {
                "word": "arrival",
                "isClicked": False,
                "isSearched": True,
                "isSensitive": False,
                "count": 1,
            },
            {
                "word": "fuck",
                "isClicked": False,
                "isSearched": True,
                "isSensitive": True,
                "count": 1,
            },
        ],
        "conversations": [
            {
                "from": "agent",
                "content_type": "text",
                "content": "hello!",
                "date": "15/03/2023",
                "time": "09:48:00",
                "sentiment": "Positive",
                "confidence": 0.97,
            },
            {
                "from": "agent",
                "content_type": "text",
                "content": "How may I help you?",
                "date": "15/03/2023",
                "time": "09:48:00",
                "sentiment": "Positive",
                "confidence": 0.87,
            },
            {
                "from": "client",
                "content_type": "text",
                "content": "May I check for the expected arrival date of my package?",
                "date": "15/03/2023",
                "time": "09:48:00",
                "sentiment": "Positive",
                "confidence": 0.47,
            },
            {
                "from": "agent",
                "content_type": "text",
                "content": "Sure! May I have your package id, please.",
                "date": "15/03/2023",
                "time": "09:48:00",
                "sentiment": "Positive",
                "confidence": 0.17,
            },
            {
                "from": "client",
                "content_type": "text",
                "content": "It's AOS1239949123.",
                "date": "15/03/2023",
                "time": "09:48:00",
                "sentiment": "Positive",
                "confidence": 0.27,
            },
            {
                "from": "agent",
                "content_type": "text",
                "content": "Got it! Hold on for a minute, please.",
                "date": "15/03/2023",
                "time": "09:48:00",
                "sentiment": "Positive",
                "confidence": 0.33,
            },
            {
                "from": "agent",
                "content_type": "text",
                "content": "It's tomorrow, which is 16/03/2023. Any other enquiries?",
                "date": "15/03/2023",
                "time": "09:48:00",
                "sentiment": "Positive",
                "confidence": 0.65,
            },
            {
                "from": "client",
                "content_type": "text",
                "content": "fuck. No thanks.",
                "date": "15/03/2023",
                "time": "09:48:00",
                "sentiment": "Negative",
                "confidence": 0.34,
            },
            {
                "from": "agent",
                "content_type": "text",
                "content": "Happy to help you.",
                "date": "15/03/2023",
                "time": "09:48:00",
                "sentiment": "Positive",
                "confidence": 0.24,
            },
            {
                "from": "agent",
                "content_type": "text",
                "content": "Happy to help you.asdnkoooooookkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkdasomdkoqmdoqwkodq mkdoqwdmkqow dmkqdo mqkwod qmkdoq mdkqod mqkoq wkdkoqw mdkqo",
                "date": "15/03/2023",
                "time": "09:48:00",
                "sentiment": "Positive",
                "confidence": 0.11,
            },
        ],
    }
