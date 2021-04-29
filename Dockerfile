FROM python:3-slim

ENV SCHEDULER_NAME="map-scheduler"
ENV PYTHONUNBUFFERED="0"

COPY * /

RUN pip3 install -r requirements.txt

CMD python3 scheduler.py
