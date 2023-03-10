from text_processing import TextProcessing
from fastapi import FastAPI
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


app = FastAPI()


@app.get("/")
def read_root():
    lines = None
    with open("./docs/index.html", "r", encoding="utf-8") as f:
        lines = "".join(f.readlines())
    return HTMLResponse(content=lines)


@app.post("/stt/audio")
def STT_Audio(query: AudioQuery):
    result = None
    sorted_word_counts = None
    MarkedWords = None

    if query.url == "testing":
        # return {"Result": "Not Applicable."}
        result = Transcribe(os.getcwd() + "/test.mp3", True).getText()
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
    MarkedWords["obj"] = markedObj.getMarkedObj()
    MarkedWords["html"] = markedObj.getMarkedHTML()

    sentiment = None
    cl = NaiveBayes().getClassifier()
    if (
        TextBlob(
            processed_result.getProcessedSentence(),
            classifier=cl,
        ).classify()
        == 1
    ):
        sentiment = "Positive"
    else:
        sentiment = "Negative"

    return {
        "id": 1,
        "text": result,
        "most_frequent_words": sorted_word_counts,
        "sensitive_words": {
            "obj": MarkedWords["obj"],
            "html": MarkedWords["html"],
        },
        "sentiment": sentiment,
    }
