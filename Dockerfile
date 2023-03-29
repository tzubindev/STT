
FROM python:3.8

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get install -y apt-utils && \
    apt-get -y install libc-dev && \
    apt-get -y install build-essential && \
    apt-get install -y freetds-dev freetds-bin && \
    apt-get install -y python3.8-dev  && \
    apt-get install -y python-distutils

RUN pip install --upgrade pip
# 
WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY pyAudioAnalysis /code/pyAudioAnalysis/

RUN pip install -e ./pyAudioAnalysis/
# 
COPY . /code/

ENV PYTHONPATH /code/

RUN python Database.py

# 
CMD ["python", "-m","uvicorn", "main:app","--port", "3001"]