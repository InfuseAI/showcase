# PrimeHub Deployment + PostgreSQL + SQLPad MLOps ecosystem.

Build up a MLOps API service echosystem

## Usage

### Step 1: Import postgresql template into PrimeHub apps and start the service
```bash
cd app_postgresql
kubectl -n hub apply -f postgresql.yaml
```

### Step 2: Deploy seldon server

Upload `./deployment/Model.py` to PrimeHub Shared files. Remember to modify the content variable.

### Step 3: Curl API and Check the Database

- Curl the API
```base
# Please modify the content variable
./sql_check/curl_seldon_server_api.sh
```

- Check the database: 
```
# Please modify the content variable
sql_check.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please specify in your PR if you want your PrimeHub app pre-installed with PrimeHub or not.

## License

Apache 2.0