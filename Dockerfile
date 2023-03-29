
FROM python:3.9

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get install -y apt-utils && \
    apt-get install -y freetds-dev && \
    apt-get install python3-distutils

RUN pip install --upgrade pip
# 
WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/

WORKDIR /pyAudioAnalysis

RUN ls .

RUN pip install -r ./code/pyAudioAnalysis/requirements.txt

RUN pip install -e .

ENV PYTHONPATH /code/

RUN python Database.py

# 
CMD ["python3.9", "-m","uvicorn", "main:app","--port", "3001"]