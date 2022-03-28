VERSION := v0.1.0-dev
IMAGE_NAME_BASE=huggingface-prepackaged
IMAGE_BASE=infuseaidev/${IMAGE_NAME_BASE}

build:
	docker build . -t ${IMAGE_BASE}:${VERSION}

push:
	docker push ${IMAGE_BASE}:${VERSION}
