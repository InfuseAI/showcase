from io import BufferedReader, BytesIO
import os
import json
import asyncio
import requests
import cv2
import streamlit as st
import av
from streamlit_webrtc import (
    RTCConfiguration,
    VideoProcessorBase,
    WebRtcMode,
    webrtc_streamer,
)

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)


class ModelVideoProcessor(VideoProcessorBase):
    def __init__(self) -> None:
        # Initial the variables.
        self.time_detect = 0
        self.response_json = {}
        self.loop = asyncio.get_event_loop()
        self.detect_new_image_bool = True

    def __request_prediction(self, image):
        # Prediction: Object detection.
        
        # Variable setting
        response = None
        self.detect_new_image_bool = False
        self.time_detect = 0
        
        # Encode the image
        ret, img_encode = cv2.imencode('.jpg', image)
        str_encode = img_encode.tostring()
        f4 = BytesIO(str_encode)
        f4.name = 'image.jpeg'
        image_bytes = BufferedReader(f4)
        files = {
            'binData': ('image.jpeg', image_bytes),
        }
        
        # Give the request to PrimeHub Deployment API.
        response = requests.post(os.getenv("PRIMEHUB_MODEL_DEPLOYMENT"), files=files)
        return response

    def __callback(self, future):
        # Get the result and replace the old detect information.
        response = future.result()
        self.response_json = json.loads(
            response.content.decode("utf-8"))['jsonData']['output']
        self.detect_new_image_bool = True

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        # Image detection process.
        
        # Variable setting.
        self.time_detect += 1
        image = frame.to_ndarray(format="bgr24")
        if self.detect_new_image_bool is True:
            future = self.loop.run_in_executor(
                None, self.__request_prediction, image)
            future.add_done_callback(self.__callback)
        
        # Draw the result.
        for rectangle in self.response_json:
            pt1 = (rectangle[2], rectangle[4])
            pt2 = (rectangle[3], rectangle[5])
            cv2.rectangle(image, pt1, pt2, (0, 0, 255), 1)
            cv2.putText(image,
                        f"{rectangle[0]}[{rectangle[1]}]",
                        (pt1[0], pt1[1] - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 0, 0),
                        1
                        )
            cv2.putText(image,
                        f"{self.time_detect}",
                        (5, 20),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 0, 0),
                        1
                        )
        return av.VideoFrame.from_ndarray(image, format="bgr24")

# Streamlit and Streamlit webrtc pipeline.
st.header("Primehub Showcase", anchor=None)
st.caption("webcam live streaming for PrimeHub deployment image detection. You can use this dashboard to do the defect detection.")

webrtc_streamer(
    key="example",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=RTC_CONFIGURATION,
    video_processor_factory=ModelVideoProcessor,
    media_stream_constraints={"video": True, "audio": False}
)

st.text("Made by InfuseAI.")
