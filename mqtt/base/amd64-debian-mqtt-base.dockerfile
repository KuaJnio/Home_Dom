FROM debian-rdt:5000/amd64-debian-base

RUN apt-get update; apt-get install -y mosquitto 
