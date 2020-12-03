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

  cat <<EOF > $TMP_DIR/app.yaml
  runtime: custom
  env: flex
  env_variables:
    SCRIPT: "$SCRIPT"
    ENABLE_FLASK: "true"
  manual_scaling:
    instances: 1
  resources:
    cpu: 1
    memory_gb: 0.5
    disk_size_gb: 10
EOF

  # deploy
  pushd $TMP_DIR
    gcloud app deploy --image-url $GCR_PATH -q
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


