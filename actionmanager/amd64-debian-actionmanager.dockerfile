FROM debian-rdt:5000/amd64-debian-actionmanager-base

ENTRYPOINT ["/usr/bin/python", "main.py"]
WORKDIR /root/actionmanager

COPY source .
