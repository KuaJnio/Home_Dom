FROM resin/rpi-raspbian 

RUN apt-get update
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-dev
RUN apt-get install -y build-essential
RUN apt-get install -y mosquitto mpg123 alsa-utils

COPY requirements.txt /root

RUN pip3 install -U -r /root/requirements.txt
