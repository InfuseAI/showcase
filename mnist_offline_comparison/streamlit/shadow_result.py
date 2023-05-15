import mlflow.pyfunc
import numpy as np
import cv2
import pandas as pd
import mlflow

class ShadowDeployment:
    def __init__(self):
        self.df = pd.read_csv("./data/result.csv")
        self.experiment_name = "mnist_train"
        self.current_experiment = dict(mlflow.get_experiment_by_name(self.experiment_name))
        self.experiment_id = self.current_experiment['experiment_id']
        self.client = mlflow.tracking.MlflowClient()
        self.runs = self.client.search_runs(self.experiment_id)
        self.run_id_list = []
        self.shadow_df = pd.DataFrame()

    def load_model(self):
        for run in self.runs:
            self.run_id_list.append(run.info.run_id)

        self.shadow_df['answer'] = self.df['answer']
        self.shadow_df['image_path'] = self.df['image_path']

        for run_id in self.run_id_list:
            print("Run ID: {}".format(run_id))
            model_uri = "runs:/{}/model".format(run_id)
            loaded_model = mlflow.pyfunc.load_model(model_uri)
            self.shadow_df['result_{}'.format(run_id)] = -1
            for i, image_path in enumerate(list(self.df['image_path'])):
                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                resized_image = cv2.resize(image, (28, 28), interpolation=cv2.INTER_AREA)
                input_data = np.array(resized_image, dtype=np.float32).reshape(1, 28*28) / 255.0
                predicted_label = loaded_model.predict(input_data).tolist()[0]
                result = predicted_label.index(max(predicted_label))
                print("Predicted label: {}".format(result))
                self.shadow_df['result_{}'.format(run_id)][i] = result
        self.shadow_df.to_csv("./result/shadow_deployment_result.csv", index=False)

if __name__ == "__main__":
    sd = ShadowDeployment()
    sd.load_model()
