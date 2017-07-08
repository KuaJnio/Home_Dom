#!/bin/bash
REGISTRY="debian-rdt:5000/"
ARCH="amd64"
OS="debian"
NAME="enocean"
IMAGE_BASE="${REGISTRY}${ARCH}-${OS}-${NAME}-base"
IMAGE="debian-rdt:5000/${ARCH}-${OS}-${NAME}"
REMOTE="docker -H debian-rdt:2375"
DOCKERFILE="${ARCH}-${OS}-${NAME}.dockerfile"
RUN="run -d --restart always --name ${NAME} ${IMAGE} main.py 192.168.1.100 1883 enocean.inputs"

docker build --pull -t ${IMAGE} -f ${DOCKERFILE} .
docker push ${IMAGE}

${REMOTE} rm -f ${NAME}
${REMOTE} pull ${IMAGE}
${REMOTE} ${RUN}



