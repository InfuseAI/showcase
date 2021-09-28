import os
import pandas as pd
from pycaret.classification import *

class Model:
    def __init__(self, model_uri):
        print(model_uri)
        print(os.listdir(model_uri))

        self.loaded = False
        self.model_uri = model_uri
        self.column_list = ['age', 'job', 'marital', 'education', 'default', 'balance', 'housing', 'loan', 'contact', 'day', 'month', 'duration', 'campaign', 'pdays', 'previous', 'poutcome', 'deposit']

    def load(self):
        self._model = load_model(os.path.join(self.model_uri, 'model'))
        self.loaded = True

    def predict(self, X, feature_names=None, meta=None):
        if not self.loaded:
            self.load()
        print("X: \n{}\n".format(X))
        data_unseen = pd.DataFrame(X, columns = self.column_list)
        print("data_unseen: \n{}\n".format(data_unseen))
        result = predict_model(self._model, data = data_unseen)
        print("result: \n{}\n".format(result))
        output = result.to_json()
        print("output: \n{}\n".format(output))
        return output
