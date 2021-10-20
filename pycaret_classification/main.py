#!/usr/bin/env python
# coding: utf-8
import os
import argparse
from src.pycaret_classification_training import PycaretClassificationTraining

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", help="The path of csv data.", type=str, default = "automl")
    parser.add_argument("--data_path", help="The path of csv data.", type=str, default = "./data/bank.csv")
    parser.add_argument("--target_column", help="The column name of target.", type=str, default = "deposit")
    parser.add_argument("--mlflow_experiment_name", help="The name of MLFlow experiment.", type=str, default = "bank_dataset")
    parser.add_argument("--model_name", help="The specific model name.", type=str, default = "lightgbm")
    parser.add_argument("--test_model_path", help="The path of model which is needed to test.", type=str)
    args = parser.parse_args()
    
    pycaret_classification_training = PycaretClassificationTraining(args.data_path)
    if args.mode == "automl":
        pycaret_classification_training.automl_training(args.target_column, args.mlflow_experiment_name)
    elif args.mode == "specific":
        pycaret_classification_training.specific_training(args.model_name)
    elif args.mode == "test":
        pycaret_classification_training.specific_training(args.test_model_path)