import os
import json
from PIL import Image
import requests
import streamlit as st
import cv2
import numpy as np

endpoint = os.getenv('ENDPOINT', '')
face_detection_xml_file = os.getenv('FACE_DETECTION_XML_FILE', '')


@st.cache(show_spinner=False, suppress_st_warning=True)  # Avoid redundant API calls for the same image
def inference(imageBytes):
    response = requests.post(endpoint, files={'binData': imageBytes})
    score = response.json()['data']['tensor']['values'][0]
    return score


def main():
    face_model = cv2.CascadeClassifier(face_detection_xml_file)
    
    st.set_page_config(layout='wide')

    st.title('Mask Detection')

    if not endpoint:
        st.error('Environment variable: ENDPOINT not set')
        return

    files = st.sidebar.file_uploader('Upload Images:', type=['png', 'jpeg', 'jpg'], accept_multiple_files=True)
    
    threshold = st.sidebar.slider('Threshold:', min_value=0.0, max_value=1.0, value=0.6, step=0.05)

    st.text("Mask detection:")
    col_size = st.sidebar.selectbox('Detection images Column Size:', range(1, 11), index=6)
    cols = st.columns(col_size)
    
    st.text("Original Images:")
    col_size_original = st.sidebar.selectbox('Original images Column Size:', range(1, 11), index=3)
    cols_original = st.columns(col_size_original)
    

    if files:
        num_face = 0
        cells = []
        # Display
        for i, file in enumerate(reversed(files)):
            img = np.array(Image.open(file).convert('RGB')) 
            cols_original[i % col_size].image(img)
            cols_original[i % col_size].text("No. {}".format(i))
            
            img = cv2.cvtColor(img, cv2.IMREAD_GRAYSCALE)
            
            faces = face_model.detectMultiScale(img,scaleFactor=1.1, minNeighbors=4) #returns a list of (x,y,w,h) tuples
            for i in range(len(faces)):
                (x,y,w,h) = faces[i]
                crop = img[y:y+h,x:x+w]
                crop = cv2.resize(crop,(128,128))
                cropBytes = cv2.imencode('.jpg', crop)[1].tobytes()
                files = {
                    'binData': crop,
                }
                cols[num_face % col_size].text("No. {}".format(num_face))
                cols[num_face % col_size].image(crop)
                cells.append({
                    'image': cropBytes,
                    'text': cols[num_face % col_size].info('Processing')
                })
                num_face += 1
        # Inference and show result
        for cell in reversed(cells):
            score = inference(cell['image'])
            if score > threshold:
                cell['text'].success(f'Wear the mask.')
            else:
                cell['text'].error(f'Not wear the mask.')


if __name__ == "__main__":
    main()
