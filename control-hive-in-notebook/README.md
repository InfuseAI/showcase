# Control Hive server in PrimeHub Notebook

## Prerequisites

- PrimeHub
- Hive server

## Usage

Build docker image: 
```
$ docker build -t <workspace-name>/jupyter-notebook-hive:0.1.0 .
```

Push docker image into docker registry:
Note: If you want to push the docker image into the docker registry platform, then you need to use docker login or nerdctl login to login into the platform.
```
$ docker push <workspace-name>/jupyter-notebook-hive:0.1.0
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please specify in your PR if you want your PrimeHub app pre-installed with PrimeHub or not.

## License

Apache 2.0