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
  # set up deployment directory
  # copy over local copy of library
  rsync -av $REPO_ROOT $TMP_DIR/python-logging \
    --exclude tests --exclude .nox --exclude samples \
    --exclude docs --exclude __pycache__
  # copy test scripts
  cp $SCRIPT_DIR/$SCRIPT $TMP_DIR
  cp $SCRIPT_DIR/logger_tests.py $TMP_DIR/
  cp $SCRIPT_DIR/requirements.txt $TMP_DIR
  # build app.yaml
  cat <<EOF > $TMP_DIR/app.yaml
    runtime: python
    env: flex
    entrypoint: python $SCRIPT
    runtime_config:
      python_version: 3
    manual_scaling:
      instances: 1
    resources:
      cpu: 1
      memory_gb: 0.5
      disk_size_gb: 10
    env_variables:
      ENABLE_FLASK: "true"
EOF
  # deploy
  pushd $TMP_DIR
    gcloud app deploy -q
  popd
  GAE_HOST=https://$(gcloud app describe --format="value(defaultHostname)")
  gcloud pubsub subscriptions create appengine \
    --topic logging-test \
    --push-endpoint $GAE_HOST \
    --ack-deadline 10 2> /dev/null | cat
}

filter-string() {
  echo "pass"
}

logs() {
  echo "pass"
}

SCRIPT_DIR=$(realpath $(dirname "$0"))
source $SCRIPT_DIR/common.sh
