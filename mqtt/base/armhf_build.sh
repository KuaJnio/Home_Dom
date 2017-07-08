#!/bin/bash
REGISTRY="debian-rdt:5000/"
ARCH="armhf"
OS="raspbian"
NAME="mqtt"
IMAGE="${REGISTRY}${ARCH}-${OS}-${NAME}-base"
DOCKERFILE="${ARCH}-${OS}-${NAME}-base.dockerfile"

docker build --pull -t ${IMAGE} -f ${DOCKERFILE} .
docker push ${IMAGE}
