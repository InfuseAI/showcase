import os
import pandas as pd
from sqlalchemy import create_engine


class Model():
    def __init__(self, model_uri):
        print("model uri: {}".format(model_uri))
        print("List of the model uri: {}".format(os.listdir(model_uri)))

        self.model_uri = model_uri
        self.engine = None
        self.postgresql_setting()

    def postgresql_setting(self):
        # Need to change the information
        pgusername = "<postgres-username>"
        pgpassword = "<postgres-password>"
        pgendpoints = "<postgres-service-endpoints>"

        engine = create_engine(
            'postgresql://{}:{}@{}'.format(pgusername, pgpassword, pgendpoints), echo=True)
        self.cnx = engine.connect()

    def load(self):
        # Please write the load model method below.
        pass

    def predict(self, X, feature_names=None, meta=None):
        result = {}
        # Please write the prediction method below.
        df = pd.DataFrame(X, columns=["name", "age"])
        df.to_sql("profile", self.cnx, index=False, if_exists="append")

        result = {"result": "Done"}

        return result
