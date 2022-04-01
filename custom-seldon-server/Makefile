VERSION := v0.1.0
IMAGE_NAME_BASE=custom-seldon-server
IMAGE_BASE=infuseaidev/${IMAGE_NAME_BASE}

build-%:
	docker build -t ${IMAGE_BASE}:${*}-server-${VERSION} ./docker/${*}/

push-%:
	docker push ${IMAGE_BASE}:${*}-server-${VERSION}
