FROM registry:5000/armhf-base

#RUN pip install --upgrade pip; pip install paho-mqtt

ENTRYPOINT ["/usr/bin/python", "-u", "main.py"]
WORKDIR /root/ping

COPY source .
