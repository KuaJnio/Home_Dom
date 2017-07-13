FROM debian-rdt:5000/armhf-raspbian-lifx-base

ENTRYPOINT ["/usr/bin/python", "-u", "main.py"]
WORKDIR /root/lifx

COPY source .
