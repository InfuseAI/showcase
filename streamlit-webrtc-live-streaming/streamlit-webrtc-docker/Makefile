VERSION := v0.1.0
IMAGE_NAME_BASE=streamlit-webrtc-app
IMAGE_BASE=infuseaidev/${IMAGE_NAME_BASE}

build:
	docker build . -t ${IMAGE_BASE}:${VERSION}

push:
	docker push ${IMAGE_BASE}:${VERSION}