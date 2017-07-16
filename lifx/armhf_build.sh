#!/bin/bash
REGISTRY="registry:5000"
ARCH="armhf"
NAME="lifx"
IMAGE="${REGISTRY}/${ARCH}-${OS}-${NAME}"
REMOTE="docker -H homedom:2375"
DOCKERFILE="${ARCH}-${NAME}.dockerfile"
RUN="run -d --restart always --net host --name ${NAME} ${IMAGE} homedom 1883"

docker build --pull -t ${IMAGE} -f ${DOCKERFILE} .
docker push ${IMAGE}

${REMOTE} rm -f ${NAME}
${REMOTE} pull ${IMAGE}
${REMOTE} ${RUN}
${REMOTE} logs ${NAME}
#${REMOTE} rm -f ${NAME}
