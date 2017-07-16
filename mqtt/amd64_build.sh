#!/bin/bash
REGISTRY="registry:5000"
ARCH="amd64"
NAME="mqtt"
IMAGE="${REGISTRY}/${ARCH}-${NAME}"
REMOTE="docker -H homedom-server:2375"
DOCKERFILE="${ARCH}-${NAME}.dockerfile"
RUN="run -d --restart always --name ${NAME} -p 1883:1883 ${IMAGE}"

docker build --pull -t ${IMAGE} -f ${DOCKERFILE} .
docker push ${IMAGE}

${REMOTE} rm -f ${NAME}
${REMOTE} pull ${IMAGE}
${REMOTE} ${RUN}
${REMOTE} logs ${NAME}
${REMOTE} rm -f ${NAME}
