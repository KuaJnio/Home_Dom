#!/bin/bash
REGISTRY="registry:5000"
ARCH="armhf"
IMAGE="${REGISTRY}/${ARCH}-base"
DOCKERFILE="${ARCH}-base.dockerfile"

docker build -t ${IMAGE} -f ${DOCKERFILE} .
docker push ${IMAGE}
