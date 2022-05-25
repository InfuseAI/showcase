#!/bin/bash

function email_transfer(){
    USERNAME="${USER_INPUT//@/-40}"
    USERNAME="${USERNAME//_/-5f}"
    USERNAME="${USERNAME//./-2e}"
}

function pvc_mount_status(){
    PVC_DESCRIBE_CONTENT=$(kubectl -n hub describe pvc claim-$USERNAME)
    if [[ $PVC_DESCRIBE_CONTENT == *"Used By:"* ]]; then
      PVC_MOUNT_STATUS=$(kubectl -n hub describe pvc claim-$USERNAME | grep 'Used By:' | cut -c 13- )
    else
      PVC_MOUNT_STATUS=$(kubectl -n hub describe pvc claim-$USERNAME | grep 'Mounted By:' | cut -c 16- )
    fi
}

function pv_information() {
    PV_NAME=$(kubectl get pv | grep -e "hub/claim-$USERNAME " | awk '{print $1}')
}

function pvc_information() {
    PVC_NAME=$(kubectl -n hub get pvc | grep -e "^claim-$USERNAME " | awk '{print $1}')
}

function pvc_capacity_information() {
    PVC_CAPACITY=$(kubectl -n hub get pvc | grep -e "^claim-$USERNAME " | awk '{print $4}')
}

function delete_old_pvc(){
    echo "=== Remove pvc ==="
    kubectl -n hub delete pvc $PVC_NAME
}

function check_pv_not_relate_pvc() {
    sts_pv=$(kubectl -n hub get pv | grep $PV_NAME | awk '{print $5}')
    echo "* Current pv status: " $sts_pv
    echo "=== remove claimRef from pv ==="
    kubectl patch pv $PV_NAME -p '{"spec":{"claimRef":null}}'
    sts_pv=$(kubectl -n hub get pv | grep $PV_NAME | awk '{print $5}')
    echo "* Current pv status: " $sts_pv
}

function create_temp_claim_yaml(){
    echo """apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: claim-old-$USERNAME
  namespace: hub
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: $PVC_CAPACITY # must be the same size
  storageClassName: rook-block
  volumeMode: Filesystem
  volumeName: $PV_NAME""" > temp-claim-$USERNAME.yaml
}

function create_new_claim_yaml(){
    echo """apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  annotations:
    hub.jupyter.org/username: $USERNAME
    volume.beta.kubernetes.io/storage-class: rook-block
  labels:
    app: jupyterhub
    chart: jupyterhub-0.10.6
    component: singleuser-storage
    heritage: jupyterhub
    release: primehub
  name: claim-$USERNAME
  namespace: hub
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: $PVC_CAPACITY # same size
  storageClassName: rook-block
  volumeMode: Filesystem""" > claim-$USERNAME.yaml
}

function rsync_files(){
    while true
    do
      echo "* Pod status: " $(kubectl -n hub get pod -l app=rsync-pvc | grep rsync-pvc | awk '{print $3}')
      if [ $(kubectl -n hub get pod -l app=rsync-pvc | grep rsync-pvc | awk '{print $3}') = "Running" ]; then
        echo "* Successfully start the rsync-pvc pod."
        kubectl -n hub exec -it $(kubectl -n hub get pod -l app=rsync-pvc | cut -d' ' -f1 | grep -v NAME) -- bash -c "apt-get update && apt-get install -yq rsync && rsync -avP /pvcs/claim-old-$USERNAME/ /pvcs/claim-$USERNAME/"
        break
      else
        sleep 3
      fi
    done
}

function delete_rsync_pod(){
    kubectl -n hub delete deploy rsync-pvc
    while true
    do
      echo "* Pod status: " $(kubectl -n hub get pod -l app=rsync-pvc | grep rsync-pvc | awk '{print $3}')
      if [ -z $(kubectl -n hub get pod -l app=rsync-pvc | grep rsync-pvc | awk '{print $3}') ]; then
        echo "* Successfully shutdown the rsync-pvc pod."
        break
      else
        sleep 5
      fi
    done
}

USER_INPUT=$1
USERNAME=$1
email_transfer
echo "===== [Part1] Prerequisite check. ====="
echo "=== Username information ==="
echo "Username: $USERNAME"
pv_information
pvc_mount_status
echo "=== pvc mount status ==="
echo "PVC mount status: $PVC_MOUNT_STATUS"

if [ $(command -v jq) == "" ]; then
  echo "[ERROR] Please install jq linux package."
elif [ -z $PV_NAME ]; then
  echo "[ERROR] The username is not correct. Please check the username: $USERNAME"
elif [ $PVC_MOUNT_STATUS != "<none>" ]; then
  echo "[ERROR] Please check your PrimeHub Notebook is successfully shutdown."
elif [ ! -f "$HOME/bin/kubectl-mountpvc" ]; then
  echo "[ERROR] Please check kubectl-mountpvc file is put in bin folder."
else
  echo -e "===== [Done] Prerequisite check. =====\n"
  echo "===== [Part2] Check the user information. ====="
  echo "=== Username information ==="
  echo "Username: $USERNAME"

  echo "=== PV name information ==="
  echo "PV name: $PV_NAME"

  echo "=== PVC name information ==="
  pvc_information
  echo "PVC name: $PVC_NAME"

  echo "=== PVC capacity information ==="
  pvc_capacity_information
  echo "PVC capacity: $PVC_CAPACITY"

  read -p "Please check the information is correct (y): " correct_bool
  if [ $correct_bool = "y" ]; then
    echo -e "===== [Done] Check the user information. =====\n"
    echo "===== [Part3] Rebuild PVC process ====="
    echo "=== Step 1/8: Delete user pvc and check PV status is available ==="
    delete_old_pvc
    check_pv_not_relate_pvc

    echo "=== Step 2/8: Create a temp pvc ==="
    create_temp_claim_yaml

    echo "=== Step 3/8: Apply a temp pvc ==="
    kubectl -n hub apply -f temp-claim-$USERNAME.yaml

    echo "=== Step 4/8: Create a new pvc ==="
    create_new_claim_yaml

    echo "=== Step 5/8: Apply a new pvc ==="
    kubectl -n hub apply -f claim-$USERNAME.yaml

    echo "=== Step 6/8: Mount PVC ==="
    kubectl mountpvc --pvc claim-$USERNAME --pvc claim-old-$USERNAME \
        -n hub rsync-pvc --image ubuntu:18.04 --command -- sleep 100000 | kubectl apply -f -

    echo "=== Step 7/8: Rsync data from old to new. ==="
    rsync_files

    echo "=== Step 8/8: Delete rsync pod ==="
    delete_rsync_pod
    echo "===== [Done] Rebuild PVC process ====="
  else
    echo "[Error] Stop the process. Please restart the script and check the correct information."
  fi
fi