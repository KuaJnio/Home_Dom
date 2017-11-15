#!/bin/bash

NAME="mqtt"
ARCH="armhf"
TARGET="homedom-${ARCH}-touch"
REGISTRY="registry:5000"
IMAGE="${REGISTRY}/${ARCH}-${NAME}"
REMOTE="docker -H ${TARGET}:2375"
RUN="run -d --restart always --name ${NAME} -p 1883:1883 -p 1884:1884 ${IMAGE}"

docker build --no-cache --pull -t ${IMAGE} .
docker push ${IMAGE}

${REMOTE} rm -f ${NAME}
${REMOTE} pull ${IMAGE}
${REMOTE} ${RUN}
