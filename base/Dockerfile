FROM resin/rpi-raspbian 

RUN apt-get update
RUN apt-get install -y python3-pip mosquitto mpg123 alsa-utils iputils-ping
RUN python3 -m pip install -U pip
RUN python3 -m pip install -U paho-mqtt
RUN python3 -m pip install -U pyserial
RUN python3 -m pip install -U lifxlan
RUN python3 -m pip install -U influxdb
RUN python3 -m pip install -U flask
