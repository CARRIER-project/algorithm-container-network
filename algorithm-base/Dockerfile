FROM python:3-alpine

RUN mkdir /app
COPY ./requirements.txt /app/

RUN apk add iptables iputils iproute2

WORKDIR /app

RUN pip install -r requirements.txt

CMD python

