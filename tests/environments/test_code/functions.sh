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
  local RUNTIME="${2:-python37}"
  # set up deployment directory
  # copy over local copy of library
  rsync -av $REPO_ROOT $TMP_DIR/python-logging \
    --exclude tests --exclude .nox --exclude samples \
    --exclude docs --exclude __pycache__
  # copy test scripts
  cp $SCRIPT_DIR/$SCRIPT $TMP_DIR/main.py
  cp $SCRIPT_DIR/logger_tests.py $TMP_DIR/
  echo  "-e ./python-logging" | cat $SCRIPT_DIR/requirements.txt - > $TMP_DIR/requirements.txt
  # deploy function
  pushd $TMP_DIR
    gcloud functions deploy logging-test \
      --entry-point pubsub_gcf \
      --trigger-topic logging-test \
      --runtime $RUNTIME \
      --region us-west2
  popd
}

filter-string() {
  echo "pass"
}

logs() {
  echo "pass"
}

SCRIPT_DIR=$(realpath $(dirname "$0"))
source $SCRIPT_DIR/common.sh
