#!/bin/bash
set -e # exit on any failure
set -o pipefail # any step in pipe caused failure
set -u # undefined variables cause exit

GCE_INSTANCE_NAME=logging-test



destroy() {
  gcloud compute instances delete $GCE_INSTANCE_NAME -q
}

verify() {
  STATUS=$(gcloud compute instances list --filter="name~^$GCE_INSTANCE_NAME$" --format="value(STATUS)")
   if [[ $STATUS == $"RUNNING" ]]; then
     echo "TRUE"
     exit 0
   else
     echo "FALSE"
     exit 1
  fi
}

deploy() {
  build_container
  gcloud beta compute instances create-with-container \
    $GCE_INSTANCE_NAME \
    --container-image $GCR_PATH \
    --container-env SCRIPT="router.py",ENABLE_SUBSCRIBER="true"
}

SCRIPT_DIR=$(realpath $(dirname "$0"))
source $SCRIPT_DIR/common.sh
