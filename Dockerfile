
FROM python:3.8-alpine

RUN python3.8 -m pip install --upgrade pip

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get install -y apt-utils && \
    apt-get install -y freetds-dev && \
    apt-get install -y python3.8-dev

# 
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN python3.8 -m pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY . /code/

RUN python /code/Database.py

ENV PYTHONPATH /code/

# 
CMD ["python", "-m","uvicorn", "main:app","--port", "3001"]