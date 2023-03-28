
FROM python:3.9

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get install -y freetds-dev

# 
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN python Database.py

# 
COPY . /code/

ENV PYTHONPATH /code/

# 
CMD ["uvicorn", "main:app", "--port", "8081"]