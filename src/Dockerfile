FROM python:3.10-alpine

WORKDIR /app

#COPY ../.env .

COPY  . .

# RUN apt-get update\
# 	&& apt-get install -y make\
#     && apt-get install -y netcat-traditional\
# 	&& pip install --upgrade pip\
# 	&& pip install --no-cache-dir -r requirements.txt

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY  . .