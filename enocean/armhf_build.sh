#!/bin/bash
REGISTRY="debian-rdt:5000/"
ARCH="armhf"
OS="raspbian"
NAME="enocean"
IMAGE_BASE="${REGISTRY}${ARCH}-${OS}-${NAME}-base"
IMAGE="debian-rdt:5000/${ARCH}-${OS}-${NAME}"
REMOTE="docker -H homedom:2375"
DOCKERFILE="${ARCH}-${OS}-${NAME}.dockerfile"
RUN="run -d --restart always --name ${NAME} --device /dev/ttyUSB0:/dev/ttyENOCEAN ${IMAGE} homedom 1883 sensor.inputs"

docker build --pull -t ${IMAGE} -f ${DOCKERFILE} .
docker push ${IMAGE}

${REMOTE} rm -f ${NAME}
${REMOTE} pull ${IMAGE}
${REMOTE} ${RUN}
