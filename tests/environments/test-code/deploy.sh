#!/bin/bash
set -e # exit on any failure
set -o pipefail # any step in pipe caused failure
set -u # undefined variables cause exit
set -x # verbose logs

# define variables
GCR_PATH=gcr.io/sanche-testing-project/logging:latest
GKE_CLUSTER=logging-test
ZONE=us-central1-b

# ensure the working dir is the repo root
SCRIPT_DIR=$(realpath $(dirname "$0"))
REPO_ROOT=$SCRIPT_DIR/../../..
cd $REPO_ROOT

_clean_name(){
  echo $(echo "${1%%.*}" | tr ._ - | tr -dc '[:alnum:]-')
}

build_container() {
  docker build -t $GCR_PATH --file $SCRIPT_DIR/Dockerfile $REPO_ROOT
  docker push $GCR_PATH
}

deploy_cloudrun() {
  local SCRIPT="${1:-test_flask.py}"
  build_container
  gcloud config set run/platform managed
  gcloud config set run/region us-west1
  gcloud run deploy  \
    --allow-unauthenticated \
    --image $GCR_PATH \
    --update-env-vars SCRIPT=$SCRIPT \
    $(_clean_name $SCRIPT)
}

attach_or_create_gke_cluster(){
  set +e
  gcloud container clusters get-credentials $GKE_CLUSTER
  if [[ $? -ne 0 ]]; then
    echo "cluster not found. creating..."
    gcloud container clusters create $GKE_CLUSTER --zone $ZONE
  fi
  set -e
}

deploy_gke() {
  local SCRIPT="${1:-test_flask.py}"

  attach_or_create_gke_cluster
  build_container
  local TMP_FILE=$SCRIPT_DIR/gke.yaml
  cat <<EOF > $TMP_FILE
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: $(_clean_name $SCRIPT)
    spec:
      selector:
        matchLabels:
          app: $(_clean_name $SCRIPT)
      template:
        metadata:
          labels:
            app: $(_clean_name $SCRIPT)
        spec:
          containers:
          - name: $(_clean_name $SCRIPT)
            image:  $GCR_PATH
            env:
            - name: SCRIPT
              value: $SCRIPT
EOF
  # clean cluster
  set +e
  kubectl delete deployments --all
  kubectl delete -f $TMP_FILE
  set -e
  # deploy test container
  kubectl apply -f $TMP_FILE
  rm $TMP_FILE
}

deploy_functions() {
  local SCRIPT="${1:-test_plain_logs.py}"
  local RUNTIME="${2:-python37}"
  # set up deployment directory
  mkdir $SCRIPT_DIR/deployment
  mkdir $SCRIPT_DIR/deployment/python-logging
  # copy over local copy of library
  rsync -av $REPO_ROOT $SCRIPT_DIR/deployment/python-logging \
    --exclude tests --exclude .nox --exclude samples \
    --exclude docs --exclude __pycache__
  # copy test scripts
  cp $SCRIPT_DIR/$SCRIPT $SCRIPT_DIR/deployment/main.py
  echo  "-e ./python-logging" | cat $SCRIPT_DIR/requirements.txt - > $SCRIPT_DIR/deployment/requirements.txt
  # deploy function
  pushd $SCRIPT_DIR/deployment
    gcloud functions deploy $(_clean_name $SCRIPT) \
      --entry-point main \
      --trigger-http \
      --runtime $RUNTIME \
      --allow-unauthenticated
  popd
  rm -rf $SCRIPT_DIR/deployment
}

#deploy_cloudrun
#deploy_gke
deploy_functions
