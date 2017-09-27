#!/bin/bash

NAME="influxdb"
ARCH="armhf"
TARGET="homedom-${ARCH}-touch"
REGISTRY="registry:5000"
IMAGE="${REGISTRY}/${ARCH}-${NAME}"
REMOTE="docker -H ${TARGET}:2375"
RUN="run -d --restart always -v /var/influxdb:/data -p 8086:8086 --name ${NAME} ${IMAGE}"


function deploy {
	${REMOTE} ${RUN}
}  

deploy
