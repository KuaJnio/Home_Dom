FROM registry:5000/base

RUN cd /home && wget http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key
RUN apt-key add /home/mosquitto-repo.gpg.key
RUN cd /etc/apt/sources.list.d/ && wget http://repo.mosquitto.org/debian/mosquitto-jessie.list
RUN apt-get update
RUN apt-get dist-upgrade

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
WORKDIR /root/mqtt

COPY source .
