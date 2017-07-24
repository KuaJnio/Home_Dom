FROM debian

RUN apt-get update; apt-get install -y python-pip mosquitto mpg123 alsa-utils; pip install paho-mqtt; pip install pyserial; pip install lifxlan
