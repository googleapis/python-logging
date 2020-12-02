#!/bin/bash
set -e # exit on any failure
set -o pipefail # any step in pipe caused failure
set -u # undefined variables cause exit



destroy() {
  echo "pass"
}

verify() {
  echo "pass"
}

deploy() {
  local SCRIPT="${1:-router.py}"
  build_container
  gcloud config set run/platform managed
  gcloud config set run/region us-west1
  gcloud run deploy  \
    --allow-unauthenticated \
    --image $GCR_PATH \
    --update-env-vars SCRIPT=$SCRIPT \
    --update-env-vars ENABLE_FLASK=true \
    logging-test
  # create pubsub subscription
  add_service_accounts
}

filter-string() {
  echo "pass"
}

logs() {
  echo "pass"
}

SCRIPT_DIR=$(realpath $(dirname "$0"))
source $SCRIPT_DIR/common.sh
