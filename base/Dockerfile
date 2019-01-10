FROM resin/rpi-raspbian:stretch-20180801

RUN apt update
RUN apt install -y python3-pip
RUN apt install -y python3-dev
RUN apt install -y build-essential
RUN apt install -y mosquitto mpg123 alsa-utils
RUN apt install -y wget
RUN apt install -y apt-transport-https

COPY requirements.txt /root

RUN pip3 install -U -r /root/requirements.txt
