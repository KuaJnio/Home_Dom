FROM debian-rdt:5000/amd64-debian-mqtt-base

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
WORKDIR /root/mqtt

COPY source .
