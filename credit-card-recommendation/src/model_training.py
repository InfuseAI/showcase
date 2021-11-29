import time
import mlflow
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LogisticRegression


class ModelTraining:
    def __init__(self):
        experiment_name = 'credit-card-recommendation'
        self.client = mlflow.tracking.MlflowClient()
        mlflow.set_experiment(experiment_name)
        mlflow.sklearn.autolog()
        self.df = None
        self.model = None
        self.run = None
        self.dataset = {}

    def pipeline(self):
        self.data_etl()
        self.model_preprocessing()
        self.model_training()
        self.model_evaluation()
        self.model_registry(
            "{}/model/".format(self.run.info.artifact_uri), self.run.info.run_id
        )

    def data_etl(self, file_path='./data/original/train.csv'):
        drop_columns = ['ID']
        encode_columns = ['Gender', 'Is_Active', 'Occupation',
                          'Channel_Code', 'Credit_Product', 'Region_Code']
        onehot_columns = ['Gender', 'Is_Active']
        dummy_columns = ['Occupation', 'Channel_Code', 'Credit_Product']
        scalar_columns = ['Age', 'Vintage', 'Avg_Account_Balance']

        # Extraction
        self.df = pd.read_csv(file_path)

        # Transform
        # Changing the distribution of 'Avg_Account_Balance' into Log Distribution
        self.df['Avg_Account_Balance'] = np.log(self.df['Avg_Account_Balance'])
        # Dropping "ID" Column
        self.df = self.df.drop(drop_columns, axis=1)
        # Replace missing value
        self.df['Credit_Product'].replace(np.nan, 'Missing', inplace=True)
        # Label Encoding
        label_encode = LabelEncoder()
        self.df[encode_columns] = self.df[encode_columns].apply(
            label_encode.fit_transform)
        # One hot encoding
        self.df[onehot_columns] = self.df[onehot_columns].apply(
            label_encode.fit_transform)
        # Get dummy
        self.df = pd.get_dummies(data=self.df, columns=dummy_columns)
        # Standard Scaling
        ss = StandardScaler()
        self.df[scalar_columns] = ss.fit_transform(self.df[scalar_columns])

        # load_To
        self.df.to_csv(
            './data/result/data_etl_result_{}.csv'.format(time.time()))

    def model_preprocessing(self):
        label = self.df['Is_Lead']
        data = self.df.drop("Is_Lead", axis=1)

        self.dataset['x_train'], self.dataset['x_test'], self.dataset['y_train'], self.dataset['y_test'] = train_test_split(
            data, label, test_size=0.3, random_state=42)

    def model_training(self):
        clf = LogisticRegression(solver="liblinear", random_state=42)
        with mlflow.start_run() as self.run:
            self.model = clf.fit(
                self.dataset['x_train'], self.dataset['y_train'])

    def model_evaluation(self):
        pred_log = self.model.predict_proba(self.dataset['x_test'])[:, 1]
        score = roc_auc_score(self.dataset['y_test'], pred_log)
        print("Logistic Regression :", score)

    def model_registry(self, model_path, model_run_id):
        registry_name = "credit-card-recommendation"
        try:
            self.client.create_registered_model(registry_name)
        except Exception:
            print("You are already create the registry model.")

        result = self.client.create_model_version(
            name=registry_name, source=model_path, run_id=model_run_id
        )
        print("Status: {}.".format(result.status))
        print("Version: {}.".format(result.version))
