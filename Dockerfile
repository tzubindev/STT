
FROM python:3.8

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get install -y apt-utils && \
    apt-get install -y freetds-dev freetds-bin && \
    apt-get install -y python3.8-dev 

RUN pip install --upgrade pip
# 
WORKDIR /code

RUN python3.8 -m pip install --no-cache-dir --upgrade -r ./requirements.txt

RUN pip install -e ./pyAudioAnalysis
# 
# COPY . /code/

RUN python Database.py

# 
CMD ["python", "-m","uvicorn", "main:app","--port", "3001"]