#!/bin/bash

NAME="actionmanager"
ARCH="amd64"

REGISTRY="registry:5000"
if [ "${ARCH}" == "amd64" ]
then
  TARGET="homedom-server"
elif [ "${ARCH}" == "armhf" ]
then
  TARGET="homedom"
fi
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
