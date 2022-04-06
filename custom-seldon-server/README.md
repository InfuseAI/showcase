# Custom seldon server

## Prerequisites

- PrimeHub Platform which can deploy model.
- Install make in Linux environment.
- Docker image registry.

    
## Usage

- Four model type of the custom seldon server
1. tensorflow
2. pytorch
3. sklearn
4. huggingface
5. base

- Build docker images
```bash
make build-<model-type>
```

- Push to docker image registry.
```
make push-<model-type>
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please specify in your PR if you want your PrimeHub app pre-installed with PrimeHub or not.

## License

Apache 2.0