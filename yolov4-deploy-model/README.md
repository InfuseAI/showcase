# Pycaret Classification Showcase

## Prerequisites

- PrimeHub Version 3.9.0+.
- PrimeHub-SDK Version: v0.3.5+
    
## Usage

### Step 1: Build the jupyter environment docker image.
```bash
cd jupyter
docker build -t <dockerhub-name>/jupyter-tensorflow-yolov4-transfer .
docker push <dockerhub-name>/jupyter-tensorflow-yolov4-transfer
```

### Step 2: Build the seldom server docker image. (Optional)
```bash
cd jupyter
docker build -t <dockerhub-name>/seldon-server-yolov4 .
docker push <dockerhub-name>/seldon-server-yolov4
```

### Step 3: Run the jupyter notebook.

1. Put the `yolov4` folder into PrimeHub notebook
2. Check the `./yolov4/deploy_pipeline.ipynb` file
3. Modify the variable and set the PrimeHub SDK.
4. Run the ipython notebook.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please specify in your PR if you want your PrimeHub app pre-installed with PrimeHub or not.

## License

Apache 2.0