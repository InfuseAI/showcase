# From python docker image
FROM python:3.7-slim
WORKDIR /app

# Install seldon-core
RUN pip install seldon-core==1.13.1

# Install python package that seldon server need to use.
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Expose the ports
EXPOSE 5000
EXPOSE 9000

# Run the seldon server.
COPY ./start_service.sh /app/start_service.sh
RUN chmod 755 /app/start_service.sh
CMD exec /app/start_service.sh
