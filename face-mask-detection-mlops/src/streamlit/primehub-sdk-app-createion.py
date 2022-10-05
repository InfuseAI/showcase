import argparse
import uuid
from primehub import PrimeHub, PrimeHubConfig

def streamlit_create_app(primehub_group, file_path, deploy_endpoint, face_detection_xml_file):
    ph = PrimeHub(PrimeHubConfig())
    
    if ph.is_ready():
        print("PrimeHub Python SDK setup successfully")
        ph.config.set_group(primehub_group)
    else:
        print("PrimeHub Python SDK couldn't get the group information, follow the primehub sdk document to complete it")
    
    # create an application
    
    random_id = uuid.uuid4().hex[:5]

    config = {
        "templateId": "streamlit-opencv",
        "id": "face-mask-detection-streamlit-{}".format(random_id),
        "displayName": "face-mask-detection-streamlit-{}".format(random_id),
        "env": [
            {
                "name": "FILE_PATH",
                "value": file_path
            },
            {
                "name": "ENDPOINT",
                "value": deploy_endpoint
            },
            {
                "name": "FACE_DETECTION_XML_FILE",
                "value": face_detection_xml_file
            }
        ],
        "instanceType": "cpu-1",
        "scope": "group"
    }
    
    result = ph.apps.create(config)
    app = result['id']
    print(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Streamlit app creation",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--primehub_group', '-g', type=str, required=True, help='The PrimeHub group name')
    parser.add_argument('--file_path', '-f', type=str, required=True, help='streamlit file path')
    parser.add_argument('--deployment_endpoint', '-d', type=str, required=True, help='deployment endpoint url')
    parser.add_argument('--face_detection_xml_file', '-x', type=str, required=True, help='face detection xml file path')
    
    args = parser.parse_args()
    streamlit_create_app(args.primehub_group, args.file_path, args.deployment_endpoint, args.face_detection_xml_file)