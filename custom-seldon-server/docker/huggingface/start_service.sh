echo "======================"
echo "[1/2] Copy the deployment code."
cp -r /mnt/models/* /app/
echo "Current file:"
ls
echo "======================"
echo "[2/2] Start the seldon service"
seldon-core-microservice Model --service-type MODEL --persistence 0 --access-log
echo "======================"