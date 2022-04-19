curl --request POST <PrimeHub-deployment-URL> \
--header 'Content-Type: application/json' \
--data-raw '{
    "data": {
        "ndarray": [["hlb", 30], ["simon", 27], ["Jimmy", 29]]
    }
}'