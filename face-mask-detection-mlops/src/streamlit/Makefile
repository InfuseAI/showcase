PRIMEHUB_GROUP=InfuseAI
STREAMLIT_FILE_PATH=/project/<group-name>/face-mask-detection-mlops/src/streamlit/mask_detection_streamlit_core.py
PRIMEHUB_DEPLOYMENT_ENDPOINT=<endpoint-url>
FACE_DETECTION_XML_FILE=/project/<group-name>/face-mask-detection-mlops/src/streamlit/face-model/haarcascade_frontalface_default.xml

create-app:
	python primehub-sdk-app-createion.py -f ${STREAMLIT_FILE_PATH} -d ${PRIMEHUB_DEPLOYMENT_ENDPOINT} -g ${PRIMEHUB_GROUP} -x ${FACE_DETECTION_XML_FILE}