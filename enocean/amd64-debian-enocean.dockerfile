FROM debian-rdt:5000/amd64-debian-enocean-base

ENTRYPOINT ["/usr/bin/python"]
WORKDIR /root/encoean

COPY source .
