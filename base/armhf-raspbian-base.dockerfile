FROM resin/rpi-raspbian 

RUN apt-get update; apt-get install -y vim python-pip subversion subversion-tools git
