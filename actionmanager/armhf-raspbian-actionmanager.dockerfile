FROM debian-rdt:5000/armhf-raspbian-actionmanager-base

ENTRYPOINT ["/usr/bin/python", "main.py"]
WORKDIR /root/actionmanager

COPY source .
