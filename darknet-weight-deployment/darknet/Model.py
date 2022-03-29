import json
import darknet
import cv2
import numpy as np
from image_process import image_detection, cvDrawBoxes


class Model(object):
    def __init__(self, model_uri='/mnt/models'):
        self.model_uri = model_uri
        self.network = None
        self.class_name = None
        self.class_colors = None
        # returns JSON object as a dictionary
        with open('{}/model.json'.format(self.model_uri)) as f:
            self.model_information = json.load(f)

    def load(self):
        print("====== Start loading yolo model ======")
        # Load darknet model
        self.network, self.class_name, self.class_colors = darknet.load_network(
            "{}/{}".format(self.model_uri,
                           self.model_information['model_cfg']),
            "{}/{}".format(self.model_uri,
                           self.model_information['label_data']),
            "{}/{}".format(self.model_uri,
                           self.model_information['model_weight']),
            batch_size=self.model_information['batch_size']
        )
        print("====== Finish loading yolo model ======")

    def predict(self, X, feature_names=None, meta=None):
        # Load and decode the image
        input_image = np.fromstring(X, np.uint8)
        decoded_image = cv2.imdecode(input_image, cv2.IMREAD_UNCHANGED)
        # Do the image object detection
        detections_list = image_detection(
            decoded_image, self.network, self.class_name, self.class_colors, self.model_information[
                'model_threshold']
        )
        return {"output": detections_list}
