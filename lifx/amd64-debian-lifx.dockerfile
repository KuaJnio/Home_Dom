FROM debian-rdt:5000/amd64-debian-lifx-base

ENTRYPOINT ["/usr/bin/python", "main.py"]
WORKDIR /root/lifx

COPY source .
