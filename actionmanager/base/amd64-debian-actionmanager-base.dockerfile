FROM debian-rdt:5000/amd64-debian-base

RUN pip install --upgrade pip; pip install paho-mqtt
