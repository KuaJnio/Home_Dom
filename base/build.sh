#!/bin/bash

REGISTRY="registry:5000"
ARCH="armhf"
IMAGE="${REGISTRY}/${ARCH}-base"

docker build --no-cache --pull -t ${IMAGE} .
#docker push ${IMAGE}
