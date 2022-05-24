# Kubernetes operation - rebuild user volume

## Prerequisites

- Kubernetes system which contains rook-block storage.
- A PVC volume that need to rebuild it.
    
## Usage

- Step 1: check username.
```bash
$ kubectl -n hub get pvc | grep claim-<username>

claim-<username>     Bound    <pvc-name>   1Gi   RWO     rook-block     16m
```

- Step 2: rebuild user volume
```bash
$ ./rebuild-user-volume.sh <username>
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please specify in your PR if you want your PrimeHub app pre-installed with PrimeHub or not.

## License

Apache 2.0