#!/bin/bash

NAME="grafana"
ARCH="amd64"
TARGET="homedom-${ARCH}"
REGISTRY="registry:5000"
IMAGE="${REGISTRY}/${ARCH}-${NAME}"
REMOTE="docker -H ${TARGET}:2375"
RUN="run -d --restart always -p 3000:3000 --name ${NAME} ${IMAGE}"


function deploy {
	${REMOTE} ${RUN}
}  

deploy
