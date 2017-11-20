#!/bin/bash

source ../deploy.cfg

NAME="recorder"
ARCH="armhf"
TARGET="homedom-${ARCH}-touch"
REGISTRY="registry:5000"
IMAGE="${REGISTRY}/${ARCH}-${NAME}"
REMOTE="docker -H ${TARGET}:2375"
RUN="run -d --restart always --name ${NAME} ${IMAGE} $MQTT_BROKER_IP $MQTT_BROKER_PORT inputs $INFLUX_HOST $INFLUX_PORT $INFLUX_USER $INFLUX_PASSWD $INFLUX_DATABASE"

docker build --no-cache --pull -t ${IMAGE} .
docker push ${IMAGE}

${REMOTE} rm -f ${NAME}
${REMOTE} pull ${IMAGE}
${REMOTE} ${RUN}
