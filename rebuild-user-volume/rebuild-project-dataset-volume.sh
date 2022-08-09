#!/bin/bash

function email_transfer(){
    PVC_NAME="${PVC_INPUT//@/-40}"
    PVC_NAME="${PVC_NAME//_/-5f}"
    PVC_NAME="${PVC_NAME//./-2e}"
}

function pvc_mount_status(){
    PVC_DESCRIBE_CONTENT=$(kubectl -n hub describe pvc $PVC_TYPE-$PVC_NAME)
    if [[ $PVC_DESCRIBE_CONTENT == *"Used By:"* ]]; then
      PVC_MOUNT_STATUS=$(kubectl -n hub describe pvc $PVC_TYPE-$PVC_NAME | grep 'Used By:' | cut -c 13- )
    else
      PVC_MOUNT_STATUS=$(kubectl -n hub describe pvc $PVC_TYPE-$PVC_NAME | grep 'Mounted By:' | cut -c 16- )
    fi
}

function create_script_folder(){
    if [ -d "./script/" ]; then
        echo "Directory ./script/ exists."
    else
        echo "Directory ./script/ not exists."
        mkdir ./script/
    fi
}

function export_yaml_file(){
    kubectl -n hub get pvc data-nfs-$PVC_TYPE-$PVC_NAME-0 -o yaml > ./script/data-nfs-$PVC_TYPE-$PVC_NAME-0.yaml
    kubectl -n hub get pvc $PVC_TYPE-$PVC_NAME -o yaml > ./script/$PVC_TYPE-$PVC_NAME.yaml
}

function pv_information() {
    HUB_NFS_PV_NAME=$(kubectl get pv | grep -e "hub/$PVC_TYPE-$PVC_NAME " | awk '{print $1}')
    STORAGE_PV_NAME=$(kubectl get pv | grep -e "hub/data-nfs-$PVC_TYPE-$PVC_NAME-0" | awk '{print $1}')
}

function pvc_information() {
    HUB_NFS_PVC_NAME=$(kubectl -n hub get pvc | grep -e "^$PVC_TYPE-$PVC_NAME " | awk '{print $1}')
    ### DO NOT DELETE STORAGE_PVC_NAME
    STORAGE_PVC_NAME=$(kubectl -n hub get pvc | grep -e "data-nfs-$PVC_TYPE-$PVC_NAME-0" | awk '{print $1}')
}

function pvc_capacity_information() {
    PVC_CAPACITY=$(kubectl -n hub get pvc | grep -e "^$PVC_TYPE-$PVC_NAME " | awk '{print $4}')
}

function delete_project_pvc_and_pv(){
    echo "=== Remove project/dataset pvc and pv ==="
    kubectl -n hub delete pvc $HUB_NFS_PVC_NAME
    kubectl delete pv $HUB_NFS_PV_NAME
}

function delete_data_nfs_pvc(){
    echo "=== Remove data-nfs pvc ==="
    kubectl -n hub delete pvc $STORAGE_PVC_NAME
}

function check_pv_not_relate_pvc() {
    sts_pv=$(kubectl -n hub get pv | grep $STORAGE_PV_NAME | awk '{print $5}')
    echo "* Current pv status: " $sts_pv
    echo "=== remove claimRef from pv ==="
    kubectl patch pv $STORAGE_PV_NAME -p '{"spec":{"claimRef":null}}'
    sts_pv=$(kubectl -n hub get pv | grep $STORAGE_PV_NAME | awk '{print $5}')
    echo "* Current pv status: " $sts_pv
}

function create_old_data_nfs_yaml(){
    echo """apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: old-$STORAGE_PVC_NAME
  namespace: hub
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: $PVC_CAPACITY
  storageClassName: rook-block
  volumeMode: Filesystem
  volumeName: $STORAGE_PV_NAME""" > ./script/old-$STORAGE_PVC_NAME.yaml
}

function create_new_data_nfs_yaml(){
    echo """apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  labels:
    app: primehub-group
    primehub-group: $PVC_NAME
    role: nfs-server
  name: $STORAGE_PVC_NAME
  namespace: hub
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: $PVC_CAPACITY
  storageClassName: rook-block
  volumeMode: Filesystem""" > ./script/new-$STORAGE_PVC_NAME.yaml
}

function rsync_files(){
    while true
    do
      echo "* Pod status: " $(kubectl -n hub get pod -l app=rsync-pvc | grep rsync-pvc | awk '{print $3}')
      if [ $(kubectl -n hub get pod -l app=rsync-pvc | grep rsync-pvc | awk '{print $3}') = "Running" ]; then
        echo "* Successfully start the rsync-pvc pod."
        kubectl -n hub exec -it $(kubectl -n hub get pod -l app=rsync-pvc | cut -d' ' -f1 | grep -v NAME) -- bash -c "apt-get update && apt-get install -yq rsync && rsync -avP /pvcs/old-$STORAGE_PVC_NAME/ /pvcs/$STORAGE_PVC_NAME/"
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

function create_new_project_yaml(){
    echo """apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  annotations:
    primehub-group: $PVC_NAME
    primehub-group-sc: rook-block
  name: $HUB_NFS_PVC_NAME
  namespace: hub
spec:
  accessModes:
  - ReadWriteMany
  resources:
    requests:
      storage: $PVC_CAPACITY
  selector:
    matchLabels:
      primehub-group: $PVC_NAME
      primehub-namespace: hub
  storageClassName: ''
  volumeMode: Filesystem
  volumeName: $HUB_NFS_PV_NAME""" > ./script/new-$HUB_NFS_PVC_NAME.yaml
}

function create_new_dataset_yaml(){
    echo """apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  annotations:
    primehub-group: $PVC_NAME
    primehub-group-sc: standard
  name: $HUB_NFS_PVC_NAME
  namespace: hub
spec:
  accessModes:
  - ReadWriteMany
  resources:
    requests:
      storage: $PVC_CAPACITY
  selector:
    matchLabels:
      primehub-group: $PVC_NAME
      primehub-namespace: hub
  storageClassName: ''
  volumeMode: Filesystem
  volumeName: $HUB_NFS_PV_NAME""" > ./script/new-$HUB_NFS_PVC_NAME.yaml
}

PVC_TYPE=$1
PVC_INPUT=$2
PVC_NAME=$2
email_transfer
echo "===== [Part1] Prerequisite check. ====="
echo "=== Project information ==="
echo "PVC_NAME: $PVC_TYPE-$PVC_NAME"
pv_information
pvc_information
pvc_mount_status
echo "=== pvc mount status ==="
echo "PVC mount status: $PVC_MOUNT_STATUS"
echo "=== Export the current yaml file ==="
create_script_folder
export_yaml_file

if [ $(command -v jq) == "" ]; then
  echo "[ERROR] Please install jq linux package."
elif [ -z $HUB_NFS_PV_NAME ]; then
  echo "[ERROR] The PVC_NAME is not correct. Please check the PVC_NAME: $PVC_TYPE-$PVC_NAME"
elif [ $PVC_MOUNT_STATUS != "<none>" ]; then
  echo "[ERROR] Please check your PrimeHub Notebook is successfully shutdown."
elif [ ! -f "$HOME/bin/kubectl-mountpvc" ]; then
  echo "[ERROR] Please check kubectl-mountpvc file is put in bin folder."
else
  echo -e "===== [Done] Prerequisite check. =====\n"
  echo "===== [Part2] Check the $PVC_TYPE information. ====="
  echo "=== PVC information ==="
  kubectl -n hub get pvc | grep CAPACITY
  kubectl -n hub get pvc | grep $PVC_TYPE-$PVC_NAME

  echo "=== PV information ==="
  kubectl get pv | grep CAPACITY
  kubectl get pv | grep $PVC_TYPE-$PVC_NAME

  echo "=== PVC capacity information ==="
  pvc_capacity_information
  echo "PVC capacity: $PVC_CAPACITY"

  echo "================================"

  read -p "Please check the information is correct (y): " correct_bool
  if [ $correct_bool = "y" ]; then
    echo -e "===== [Done] Check the $PVC_TYPE information. =====\n"
    echo "===== [Part3] Rebuild $PVC_TYPE PVC process ====="
    echo "=== Step 1/11: Delete $PVC_TYPE pvc and pv."
    delete_project_pvc_and_pv

    echo "=== Step 2/11: Delete data-nfs pvc and check PV status is available ==="
    delete_data_nfs_pvc
    check_pv_not_relate_pvc

    echo "=== Step 3/11: Create an old data-nfs pvc yaml file ==="
    create_old_data_nfs_yaml

    echo "=== Step 4/11: Create an new data-nfs pvc yaml file ==="
    create_new_data_nfs_yaml

    echo "=== Step 5/11: Create a new $PVC_TYPE pvc yaml file ==="
    if [ $PVC_TYPE == "project" ]; then
        create_new_project_yaml
    elif [ $PVC_TYPE == "dataset" ]; then
        create_new_dataset_yaml
    else
        echo "[Error] We did not have $PVC_TYPE PVC type. Please check the name is corrected or not."
    fi

    echo "=== Step 6/11: Apply an old data-nfs pvc yaml file ==="
    kubectl -n hub apply -f ./script/old-$STORAGE_PVC_NAME.yaml

    echo "=== Step 7/11: Apply an new data-nfs pvc yaml file ==="
    kubectl -n hub apply -f ./script/new-$STORAGE_PVC_NAME.yaml

    echo "=== Step 8/11: Mount PVC ==="
    kubectl mountpvc --pvc $STORAGE_PVC_NAME --pvc old-$STORAGE_PVC_NAME \
        -n hub rsync-pvc --image ubuntu:18.04 --command -- sleep 100000 | kubectl apply -f -

    echo "=== Step 9/11: Rsync data from old to new. ==="
    rsync_files

    echo "=== Step 10/11: Delete rsync pod ==="
    delete_rsync_pod

    echo "=== Step 11/11: Apply a new $PVC_TYPE pvc yaml file ==="
    kubectl -n hub apply -f ./script/new-$HUB_NFS_PVC_NAME.yaml

    echo "===== [Done] Rebuild $PVC_TYPE PVC process ====="
  else
    echo "[Error] Stop the process. Please restart the script and check the correct information."
  fi
fi