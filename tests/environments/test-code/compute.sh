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

filter-string() {
  INSTANCE_ID=$(gcloud compute instances list --filter="name~^$GCE_INSTANCE_NAME$" --format="value(ID)")
  echo "resource.type=\"gce_instance\" AND resource.labels.instance_id=\"$INSTANCE_ID\""
}

logs() {
  local OFFSET="${1:-10}"
  echo "resource filter: \"$(filter-string)\""
  echo "printing from last $OFFSET mins..."
  TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ"  --date "-$OFFSET min")
  gcloud logging read "$(filter-string) AND timestamp > \"$TIMESTAMP\""
}

SCRIPT_DIR=$(realpath $(dirname "$0"))
source $SCRIPT_DIR/common.sh
