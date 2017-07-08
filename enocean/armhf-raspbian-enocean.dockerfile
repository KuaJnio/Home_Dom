FROM debian-rdt:5000/armhf-raspbian-enocean-base

ENTRYPOINT ["/usr/bin/python"]
WORKDIR /root/encoean

COPY source .
