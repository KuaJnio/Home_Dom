FROM registry:5000/base

RUN apt-get update && apt-get install wget && cd /home && wget http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key && apt-key add mosquitto-repo.gpg.key && cd /etc/apt/sources.list.d/ && wget http://repo.mosquitto.org/debian/mosquitto-jessie.list && apt-get update && apt-get dist-upgrade

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
WORKDIR /root/mqtt

COPY source .
