FROM registry:5000/amd64-base

ENTRYPOINT ["/usr/bin/python", "-u", "main.py"]
WORKDIR /root/festival

COPY source .
