FROM continuumio/miniconda3

ENV SECONDARY_HOST=localhost
ENV SECONDARY_PORT=8888

RUN mkdir /app

COPY primary.py /app/
COPY requirements.txt /app/

WORKDIR /app

CMD ./primary.py

