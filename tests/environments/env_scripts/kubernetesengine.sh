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

attach_or_create_gke_cluster(){
  set +e
  gcloud container clusters get-credentials $GKE_CLUSTER
  if [[ $? -ne 0 ]]; then
    echo "cluster not found. creating..."
    gcloud container clusters create $GKE_CLUSTER \
      --zone $ZONE \
      --scopes "https://www.googleapis.com/auth/pubsub"
  fi
  set -e
}

deploy() {
  local SCRIPT="${1:-router.py}"

  attach_or_create_gke_cluster
  build_container
  cat <<EOF > $TMP_DIR/gke.yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: logging-test
    spec:
      selector:
        matchLabels:
          app: logging-test
      template:
        metadata:
          labels:
            app: logging-test
        spec:
          containers:
          - name: logging-test
            image:  $GCR_PATH
            env:
            - name: SCRIPT
              value: $SCRIPT
            - name: ENABLE_SUBSCRIBER
              value: "true"
EOF
  # clean cluster
  set +e
  kubectl delete deployments --all
  kubectl delete -f $TMP_DIR
  set -e
  # deploy test container
  kubectl apply -f $TMP_DIR
}

filter-string() {
  echo "pass"
}

