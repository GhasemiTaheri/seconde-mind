FROM  python:3.12.4-slim-bookworm AS os
LABEL authors="joojoo"

WORKDIR app/

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./src .
