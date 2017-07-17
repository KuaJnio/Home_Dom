#!/bin/bash
REGISTRY="registry:5000"
ARCH="amd64"
IMAGE="${REGISTRY}/${ARCH}-base"
DOCKERFILE="${ARCH}-base.dockerfile"

docker build --pull -t ${IMAGE} -f ${DOCKERFILE} .
docker push ${IMAGE}
