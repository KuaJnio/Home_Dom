FROM registry:5000/amd64-base

#RUN pip install --upgrade pip; pip install paho-mqtt; pip install lifxlan

ENTRYPOINT ["/usr/bin/python", "-u", "main.py"]
WORKDIR /root/lifx

COPY source .
