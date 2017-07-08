FROM debian-rdt:5000/armhf-raspbian-base

RUN apt-get update; apt-get install -y mosquitto 
