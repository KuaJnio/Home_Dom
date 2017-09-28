FROM resin/rpi-raspbian 

RUN apt-get update; apt-get install -y python-pip mosquitto mpg123 alsa-utils; pip install paho-mqtt; pip install pyserial; pip install lifxlan; pip install influxdb

RUN echo "192.168.1.19 homedom-amd64" >> /etc/hosts && echo "192.168.1.20 homedom-armhf-touch" >> /etc/hosts && echo "192.168.1.25 homedom-armhf-zero" >> /etc/hosts &&
