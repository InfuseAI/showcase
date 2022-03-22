# HuggingFace transformers Prepackaged Model Server

## 1. Build the base image

```
$ make build
```

## 2. Use base image to build image with model file

### How to use the docker image.
Create Dockerfile and change the value of `${MODEL}` to your model name (`my-model`).
```bash
# Directory structure
.
├── Dockerfile
└── my-model
    └── model.json
```
```dockerfile
# Dockerfile
FROM infuseaidev/huggingface-prepackaged:v0.1.0-dev
COPY ${MODEL} /mnt/models
```
```bash
# Build docker image
docker build -t huggingface-prepackaged-model .
```
```bash
# Run docker container
docker run --name huggingface-transformers --rm -it -p 5000:5000 huggingface-prepackaged-model
```