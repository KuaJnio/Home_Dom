#!/bin/bash

NAME="actionmanager"
ARCH="amd64"
TARGET="homedom-${ARCH}"
REGISTRY="registry:5000"
IMAGE="${REGISTRY}/${ARCH}-${NAME}"
REMOTE="docker -H ${TARGET}:2375"
DOCKERFILE="${ARCH}-${NAME}.dockerfile"
RUN="run -d --restart always --name ${NAME} ${IMAGE}"

docker build --pull -t ${IMAGE} -f ${DOCKERFILE} .
docker push ${IMAGE}

function deploy {
	${REMOTE} rm -f ${NAME}
	${REMOTE} pull ${IMAGE}
	${REMOTE} ${RUN}
	${REMOTE} logs -f ${NAME}
}  

#deploy
