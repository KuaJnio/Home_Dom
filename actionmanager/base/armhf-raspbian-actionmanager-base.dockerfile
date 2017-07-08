FROM debian-rdt:5000/armhf-raspbian-base

RUN pip install --upgrade pip; pip install paho-mqtt
