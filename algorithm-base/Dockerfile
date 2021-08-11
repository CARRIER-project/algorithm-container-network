FROM continuumio/miniconda3
RUN mkdir /app
COPY ./requirements.txt /app/

RUN apt update -y && apt install -y iptables iproute2

WORKDIR /app

RUN pip install -r requirements.txt

CMD python

