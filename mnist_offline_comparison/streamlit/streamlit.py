import json
import os

import requests
import streamlit as st

import pandas as pd
import time
from datetime import datetime

endpoint = os.getenv('ENDPOINT', '')


@st.cache(show_spinner=False, suppress_st_warning=True)  # Avoid redundant API calls for the same image
def inference(imageBytes):
    res = requests.post(endpoint, files={'binData': imageBytes})
    content = json.loads(res.content)
    answer = content['data']['tensor']['values'].index(max(content['data']['tensor']['values']))
    return answer


def main():
    st.set_page_config(page_title="MNIST App", page_icon=":pencil2:")

    st.title('MNIST Recognition Application')

    if not endpoint:
        st.error('Environment variable: ENDPOINT not set')
        return

    files = st.sidebar.file_uploader('Upload Images:', type=['png', 'jpeg', 'jpg'], accept_multiple_files=True)

    col_size = st.sidebar.selectbox('Column Size:', range(1, 11), index=4)
    cols = st.columns(col_size)
    cells = []

    options = ["Correct", "Wrong"]
    if files:
        # Display
        for i, file in enumerate(files):
            imageBytes = file.read()
            cols[i % col_size].text(file.name)
            cols[i % col_size].image(imageBytes)
            
            cells.append({
                'file': file,
                'image': imageBytes,
                'text': cols[i % col_size].info('Processing'),
                'correct': None
            })
            
            

        # Inference and show result
        for i, cell in enumerate(cells):
            answer = inference(cell['image'])
            cell['text'].success(answer)
            cell['answer'] = answer
            cell['correct'] = cols[i % col_size].text_input('Value:', '0', key=i)
            # get current date and time
            now = datetime.now()
            # format date as yyyy-mm-dd
            formatted_date = now.strftime("%Y%m%d")
            cell['date'] = formatted_date

        if st.button('Save as CSV'):
            for i, cell in enumerate(cells):
                image_file_name = "data/file/image_{}_{}.png".format(int(time.time()),i)
                # Save image to file
                with open(image_file_name, "wb") as f:
                    f.write(cell['file'].getbuffer())
                    cell['image_path'] = image_file_name
            
            # Combine the path.
            csv_path = "data/result.csv"
            
            # Change to pandas dataframe
            df = pd.DataFrame(cells)
            
            del df['text'], df['file'], df['image']
            
            # Verify the csv file is existed or not.
            if os.path.isfile(csv_path):
                df.to_csv(csv_path, mode="a", header=False, index=False)
                
                st.text("Successfully update csv file.")
            else:
                # Save to csv file.
                df.to_csv(csv_path, index=False)
                
                st.text("Successfully create csv file.")



if __name__ == "__main__":
    main()