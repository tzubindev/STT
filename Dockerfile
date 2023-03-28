
FROM python:3.9

RUN apt-get update && \
    apt-get install -y ffmpeg

# 
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN python3 -m pip install pymssql

# 
COPY . /code/

ENV PYTHONPATH /code/

# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]