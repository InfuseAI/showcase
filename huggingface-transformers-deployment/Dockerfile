FROM python:3.7-slim
COPY ./huggingface/requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
EXPOSE 9000
COPY ./huggingface /app

# Define environment variable
ENV MODEL_NAME Model
ENV SERVICE_TYPE MODEL
ENV PERSISTENCE 0

CMD exec seldon-core-microservice $MODEL_NAME --service-type $SERVICE_TYPE --persistence $PERSISTENCE --access-log
