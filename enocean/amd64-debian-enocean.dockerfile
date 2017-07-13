FROM debian-rdt:5000/amd64-debian-enocean-base

ENTRYPOINT ["/usr/bin/python","-u","main.py"]
WORKDIR /root/enocean

COPY source .
