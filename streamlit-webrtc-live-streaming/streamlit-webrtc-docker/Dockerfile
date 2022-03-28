FROM jjanzic/docker-python3-opencv

EXPOSE 8501

WORKDIR /streamlit

RUN pip install --upgrade pip
RUN pip install streamlit==1.2.0
RUN pip install streamlit-webrtc opencv-python-headless matplotlib pydub

ENTRYPOINT [ "streamlit" ]