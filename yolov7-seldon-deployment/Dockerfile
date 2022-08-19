FROM python:3.7-slim
COPY ./yolov7-seldon-core/requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
COPY ./yolov7-seldon-core/yolov7/requirements.txt /app/yolov7/requirements.txt
RUN pip install -r ./yolov7/requirements.txt

EXPOSE 5000
EXPOSE 9000
COPY ./yolov7-seldon-core/Model.py /app/Model.py
COPY ./yolov7-seldon-core/yolov7/ /app/

# Define environment variable
ENV MODEL_NAME Model
ENV SERVICE_TYPE MODEL
ENV PERSISTENCE 0

CMD exec seldon-core-microservice $MODEL_NAME --service-type $SERVICE_TYPE --persistence $PERSISTENCE --access-log