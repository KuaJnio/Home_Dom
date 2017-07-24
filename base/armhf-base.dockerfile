FROM resin/rpi-raspbian 

RUN apt-get update; apt-get install -y python-pip mosquitto mpg123; pip install paho-mqtt; pip install pyserial; pip install lifxlan
