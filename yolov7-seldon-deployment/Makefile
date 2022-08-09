VERSION := v0.1.0-dev
IMAGE_NAME_BASE=yolov7-prepackaged
IMAGE_BASE=infuseai/${IMAGE_NAME_BASE}

build:
	rm -rf ./yolov7-seldon-core/yolov7/
	git clone https://github.com/WongKinYiu/yolov7.git ./yolov7-seldon-core/yolov7/
	docker build . -t ${IMAGE_BASE}:${VERSION}

push:
	docker push ${IMAGE_BASE}:${VERSION}
