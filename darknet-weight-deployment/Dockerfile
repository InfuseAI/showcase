FROM ubuntu:bionic-20200403@sha256:b58746c8a89938b8c9f5b77de3b8cf1fe78210c696ab03a1442e235eea65d84f

RUN apt-get update -y && apt-get install -qy --no-install-recommends \
    wget \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libglib2.0-0 \
    git \
    build-essential \
    ca-certificates \
    && \
    rm -rf /var/lib/apt/lists/*

ENV PATH /opt/conda/bin:$PATH

# Install Miniconda3
ARG CONDA_VERSION=4.7.12
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-${CONDA_VERSION}-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda clean -tipsy && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc && \
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.js.map' -delete && \
    /opt/conda/bin/conda clean -afy

# This is to install desired version of Python without updating conda version
ARG PYTHON_VERSION=3.7
RUN conda install --yes python=$PYTHON_VERSION conda=$CONDA_VERSION

## The above code is from https://github.com/SeldonIO/seldon-core/blob/master/wrappers/s2i/python/Dockerfile.gpu
################################################################################################################

# Install Darknet

## Install OpenCV
RUN conda install  -c conda-forge opencv==4.5.5
RUN apt-get update -y && \
    apt-get install -qy --no-install-recommends libgl1-mesa-glx && \
    rm -rf /var/lib/apt/lists/*

## Build the darknet. Please see
## https://github.com/AlexeyAB/darknet#how-to-compile-on-linux-using-make
RUN cd / && \
    git clone https://github.com/AlexeyAB/darknet.git && \
    cd darknet && \
    sed -i 's/AVX=0/AVX=1/g' Makefile && \
    sed -i 's/OPENMP=0/OPENMP=1/g' Makefile && \
    sed -i 's/LIBSO=0/LIBSO=1/g' Makefile && \
    make

# Wrap the seldom custom image with python wrapper. Please see
# https://docs.seldon.io/projects/seldon-core/en/v1.1.0/python/python_wrapping_docker.html

## Install seldon.
RUN pip install seldon-core==1.13.1
EXPOSE 5000
EXPOSE 9000

## Install Application
COPY ./darknet/ /darknet/
WORKDIR /darknet

ENV MODEL_NAME Model
ENV SERVICE_TYPE MODEL
ENV PERSISTENCE 0

CMD exec seldon-core-microservice $MODEL_NAME --service-type $SERVICE_TYPE --persistence $PERSISTENCE
