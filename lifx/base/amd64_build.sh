#!/bin/bash
REGISTRY="debian-rdt:5000/"
ARCH="amd64"
OS="debian"
NAME="lifx"
IMAGE="${REGISTRY}${ARCH}-${OS}-${NAME}-base"
DOCKERFILE="${ARCH}-${OS}-${NAME}-base.dockerfile"

docker build --pull -t ${IMAGE} -f ${DOCKERFILE} .
docker push ${IMAGE}
