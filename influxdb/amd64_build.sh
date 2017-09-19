#!/bin/bash

NAME="influxdb"
ARCH="amd64"
TARGET="homedom-${ARCH}"
REGISTRY="registry:5000"
IMAGE="${REGISTRY}/${ARCH}-${NAME}"
REMOTE="docker -H ${TARGET}:2375"
RUN="run -d --restart always -v /var/influxdb:/data -p 8086:8086 --name ${NAME} ${IMAGE}"


function deploy {
	${REMOTE} ${RUN}
}  

deploy
