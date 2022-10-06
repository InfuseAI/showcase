import mlflow

def model_registry(run, test_accuracy):
    model_uri = "runs:/{}/model".format(run.info.run_id)

    model_registry_information = {"registry": False, "create_deploy": False}
    if test_accuracy >= 0.8:
        mv = mlflow.register_model(model_uri, "mask-detection-model")
        model_registry_information['registry'] = True
        model_registry_information['modeluri'] = "models:/{}/{}".format(mv.name, mv.version)
        if mv.version == "1":
            model_registry_information["create_deploy"] = True

    print(model_registry_information)

    return model_registry_information
