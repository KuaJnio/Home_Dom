FROM registry:5000/amd64-base

#RUN apt-get update; apt-get install -y mosquitto 

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
WORKDIR /root/mqtt

COPY source .
