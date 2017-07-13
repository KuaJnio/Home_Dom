FROM debian-rdt:5000/armhf-raspbian-enocean-base

ENTRYPOINT ["/usr/bin/python","-u","main.py"]
WORKDIR /root/enocean

COPY source .
