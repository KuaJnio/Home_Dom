FROM resin/rpi-raspbian:stretch-20180801

RUN apt update
RUN apt install -y python3-pip
RUN apt install -y python3-dev
RUN apt install -y build-essential
RUN apt install -y mosquitto
RUN apt install -y mpg123
RUN apt install -y alsa-utils
RUN apt install -y wget
RUN apt install -y apt-transport-https
RUN apt install -y libffi-dev

COPY requirements.txt /root

RUN pip3 install -U -r /root/requirements.txt

RUN mkdir /var/log/homedom
