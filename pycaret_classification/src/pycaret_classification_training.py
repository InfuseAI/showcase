import pandas as pd
from pycaret.classification import *


class PycaretClassificationTraining:
    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)

    def automl_training(self, target_column, mlflow_experiment_name):
        # Initializing setup
        clf1 = setup(
            self.df,
            target=target_column,
            log_experiment=True,
            experiment_name=mlflow_experiment_name,
            silent=True,
        )

        # Compare the model: Compare all the classification model. EX: catboost, lightgbm, svm, etc.
        best_model = compare_models()

        # Tuning the best model.
        final_best = finalize_model(best_model)

        # Record the parameter of automl value
        best = automl(optimize="Recall")

    def specific_training(self, model_name):
        # Create model
        particular_model = create_model(model_name)
        # Test: Predict model
        prediction = predict_model(particular_model)
        # Test: Evaluate model
        evaluate_model(particular_model)

    def test_model(self, model_path):
        # Part 1: Load saved model.
        saved_model = load_model(os.path.join(model_path, "model"))

        # Part 2: Arrange the testing data.
        test_data = [
            [
                "25",
                "admin.",
                "married",
                "secondary",
                "no",
                "45",
                "no",
                "no",
                "unknown",
                "5",
                "may",
                "1467",
                "1",
                "-1",
                "0",
                "unknown",
                "yes",
            ]
        ]
        data_unseen = pd.DataFrame(
            test_data,
            columns=[
                "age",
                "job",
                "marital",
                "education",
                "default",
                "balance",
                "housing",
                "loan",
                "contact",
                "day",
                "month",
                "duration",
                "campaign",
                "pdays",
                "previous",
                "poutcome",
                "deposit",
            ],
        )
        # Part 3: Use testing data to test saved model.
        prediction = predict_model(saved_model, data=data_unseen)
