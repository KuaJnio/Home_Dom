#!/bin/bash
REGISTRY="debian-rdt:5000/"
ARCH="armhf"
OS="raspbian"
IMAGE="${REGISTRY}${ARCH}-${OS}-base"
DOCKERFILE="${ARCH}-${OS}-base.dockerfile"

docker build --pull -t ${IMAGE} -f ${DOCKERFILE} .
docker push ${IMAGE}
