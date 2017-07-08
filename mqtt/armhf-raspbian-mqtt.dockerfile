FROM debian-rdt:5000/armhf-raspbian-mqtt-base

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
WORKDIR /root/mqtt

COPY source .
