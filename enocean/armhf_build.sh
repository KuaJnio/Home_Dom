#!/bin/bash
REGISTRY="registry:5000"
ARCH="armhf"
NAME="enocean"
IMAGE="${REGISTRY}/${ARCH}-${NAME}"
REMOTE="docker -H homedom:2375"
DOCKERFILE="${ARCH}-${NAME}.dockerfile"
RUN="run -d --restart always --name ${NAME} --device /dev/ttyUSB0:/dev/ttyENOCEAN ${IMAGE} homedom 1883 sensor.inputs"

docker build --pull -t ${IMAGE} -f ${DOCKERFILE} .
docker push ${IMAGE}

${REMOTE} rm -f ${NAME}
${REMOTE} pull ${IMAGE}
${REMOTE} ${RUN}
${REMOTE} logs ${NAME}
#${REMOTE} rm -f ${NAME}
