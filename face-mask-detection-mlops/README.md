# Face mask detection MLOps Pipeline
Use metaflow to demo the face mask detection model MLOps pipeline.

# How to use it?
- Step 1: Install linux package - make
```bash
sudo apt-get update
sudo apt-get -y install make
```

- Step 2: Download the dataset:
URL: https://www.kaggle.com/datasets/ashishjangra27/face-mask-12k-images-dataset
```bash
make download-data
```

- Step 3: Install python package
```bash
make install-python-packages
```

- Step 4: Show the pipeline
```bash
make show-pipeline
```

- Step 5: Run the pipeline
```bash
make run-pipeline
```
