FROM python:3.11.6-alpine

RUN apk add socat

WORKDIR /task

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x ./task.py

CMD socat "TCP-LISTEN:12345,reuseaddr,fork" "EXEC:/task/task.py"
