FROM registry:5000/amd64-base

#RUN pip install --upgrade pip; pip install paho-mqtt; pip install influxdb

ENTRYPOINT ["/usr/bin/python", "-u", "main.py"]
WORKDIR /root/recorder

COPY source .
