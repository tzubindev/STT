from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel


class Query(BaseModel):
    url: str


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/STT/")
def STT(query: Query):
    return {"result": query.url}
