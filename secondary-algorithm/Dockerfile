FROM continuumio/miniconda3

ENV PORT=8888

RUN mkdir /app

COPY secondary.py /app/
COPY requirements.txt /app/

WORKDIR /app

CMD ./secondary.py $PORT
