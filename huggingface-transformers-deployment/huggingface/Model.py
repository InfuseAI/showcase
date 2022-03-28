import os
import json
from transformers import pipeline


class Model():
    def __init__(self, model_uri):
        print(model_uri)
        print(os.listdir(model_uri))

        self.loaded = False
        self.model_uri = model_uri

    def load(self):
        print("====== Start loading model ======")
        # returns JSON object as a dictionary
        with open('{}/model.json'.format(self.model_uri)) as f:
            model_information = json.load(f)
        self.model = pipeline(**model_information)
        self.loaded = True
        print("===== Finish loading model =====")
        print("- Model information: {}".format(model_information))

    def predict(self, X, feature_names=None, meta=None):
        if not self.loaded:
            self.load()
        if isinstance(X, bytes):
            img = Image.open(BytesIO(X))
            img = np.array(img).astype(np.float32)
            X = np.copy(img)
            print("Input image.")
        else:
            print("Input: {}".format(X))

        result = {}
        for input_index, input_value in enumerate(X):
            result[input_index] = self.model(input_value)
        print("Output result: {}".format(result))

        return result
