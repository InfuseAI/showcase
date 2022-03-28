# Streamlit webrtc live stream for image detection model.

## Prerequisites

- Need a PrimeHub.
- Online Environment: In this example, we need to connect the Google RTC server.
- PrimeHub need an TLS certification. webrtc security needs to confirm the URL is in the safe environment.
    
## Usage

- Apply `./primehub-app/config/streamlit-stream.yaml` into PrimeHub Apps.
- Prepare the yolov4-tiny model.
- Deploy yolov4-tiny model in PrimeHub deployment.
- Create PrimeHub Notebook and put `./primehub-app/code/streamlit-example.py` into group volume.
- Create Primehub Apps - streamlit-stream.
- Configure webcam resource and start the streamlit-webrtc service.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please specify in your PR if you want your PrimeHub app pre-installed with PrimeHub or not.

## License

Apache 2.0