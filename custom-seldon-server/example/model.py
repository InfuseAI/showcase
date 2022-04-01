import os

class Model():
    def __init__(self, model_uri):
        print(model_uri)
        print(os.listdir(model_uri))

        self.model_uri = model_uri

    def load(self):
        # Please write load model method below.
        pass

    def predict(self, X, feature_names = None, meta = None):
        result = {"result": "Hello world."}
        # Please write the prediction method below.
        return result
