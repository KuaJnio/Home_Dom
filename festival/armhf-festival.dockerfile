FROM registry:5000/armhf-base

ENTRYPOINT ["/usr/bin/python", "-u", "main.py"]
WORKDIR /root/festival

COPY source .

