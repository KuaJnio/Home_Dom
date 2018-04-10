#!/bin/bash

NAME="config"
ARCH="armhf"
TARGET="homedom-${ARCH}-touch"
REGISTRY="registry:5000"
IMAGE="${REGISTRY}/${ARCH}-${NAME}"
REMOTE="docker -H ${TARGET}:2375"
RUN="run -d --restart always -p 8090:80 --name ${NAME} ${IMAGE}"

docker build --no-cache --pull -t ${IMAGE} .
docker push ${IMAGE}

${REMOTE} rm -f ${NAME}
${REMOTE} pull ${IMAGE}
${REMOTE} ${RUN}
