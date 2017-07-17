#!/bin/bash

NAME="enocean"
ARCH="armhf"
TARGET="homedom-${ARCH}"
REGISTRY="registry:5000"
IMAGE="${REGISTRY}/${ARCH}-${NAME}"
REMOTE="docker -H ${TARGET}:2375"
DOCKERFILE="${ARCH}-${NAME}.dockerfile"
RUN="run -d --restart always --name ${NAME} --device /dev/ttyUSB0:/dev/ttyENOCEAN ${IMAGE} homedom 1883 sensor.inputs"

docker build --pull -t ${IMAGE} -f ${DOCKERFILE} .
docker push ${IMAGE}

function deploy {
	${REMOTE} rm -f ${NAME}
	${REMOTE} pull ${IMAGE}
	${REMOTE} ${RUN}
	${REMOTE} logs -f ${NAME}
}  

deploy
