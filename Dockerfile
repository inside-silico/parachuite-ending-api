# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
FROM python:3.10.7-slim-buster
RUN apt update
RUN apt install git -y

WORKDIR /app

COPY . .

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN pip3 install git+https://github.com/franco-lamas/PyOBD --upgrade --no-cache-dir
RUN pip3 install git+https://github.com/franco-lamas/SHD --upgrade --no-cache-dir
RUN pip3 install git+https://github.com/franco-lamas/Fallen --upgrade --no-cache-dir





CMD [ "python3","-u", "app.py"]
