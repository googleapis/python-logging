#!/bin/bash
set -e # exit on any failure
set -o pipefail # any step in pipe caused failure
set -u # undefined variables cause exit
set -x # verbose logs

# clean-up function
finish() {
  rm -rf $TMP_DIR
}
trap finish EXIT

# ensure the working dir is the repo root
SCRIPT_DIR=$(realpath $(dirname "$0"))
REPO_ROOT=$SCRIPT_DIR/../../..
cd $REPO_ROOT

# define variables
GCR_PATH=gcr.io/sanche-testing-project/logging:latest
GKE_CLUSTER=logging-test
ZONE=us-central1-b
TMP_DIR=$SCRIPT_DIR/deploy-$(uuidgen)
mkdir $TMP_DIR



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
  cat <<EOF > $TMP_DIR/gke.yaml
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
  kubectl delete -f $TMP_DIR
  set -e
  # deploy test container
  kubectl apply -f $TMP_DIR
}

deploy_functions() {
  local SCRIPT="${1:-test_plain_logs.py}"
  local RUNTIME="${2:-python37}"
  # set up deployment directory
  # copy over local copy of library
  rsync -av $REPO_ROOT $TMP_DIR/python-logging \
    --exclude tests --exclude .nox --exclude samples \
    --exclude docs --exclude __pycache__
  # copy test scripts
  cp $SCRIPT_DIR/$SCRIPT $TMP_DIR/main.py
  echo  "-e ./python-logging" | cat $SCRIPT_DIR/requirements.txt - > $TMP_DIR/requirements.txt
  # deploy function
  pushd $TMP_DIR
    gcloud functions deploy $(_clean_name $SCRIPT) \
      --entry-point main \
      --trigger-http \
      --runtime $RUNTIME \
      --allow-unauthenticated
  popd
}

deploy_ae_standard() {
  local SCRIPT="${1:-test_flask.py}"
  local RUNTIME="${2:-python37}"
  # set up deployment directory
  # copy over local copy of library
  rsync -av $REPO_ROOT $TMP_DIR/python-logging \
    --exclude tests --exclude .nox --exclude samples \
    --exclude docs --exclude __pycache__
  # copy test scripts
  cp $SCRIPT_DIR/$SCRIPT $TMP_DIR/main.py
  echo  "-e ./python-logging" | cat $SCRIPT_DIR/requirements.txt - > $TMP_DIR/requirements.txt
  # build app.yaml
  cat <<EOF > $TMP_DIR/app.yaml
    runtime: $RUNTIME
EOF
  # deploy
  pushd $TMP_DIR
    gcloud app deploy -q
    gcloud app browse
  popd
}

deploy_ae_flex_python() {
  local SCRIPT="${1:-test_flask.py}"
  # set up deployment directory
  # copy over local copy of library
  rsync -av $REPO_ROOT $TMP_DIR/python-logging \
    --exclude tests --exclude .nox --exclude samples \
    --exclude docs --exclude __pycache__
  # copy test scripts
  cp $SCRIPT_DIR/$SCRIPT $TMP_DIR
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
EOF
  # deploy
  pushd $TMP_DIR
    gcloud app deploy -q
    gcloud app browse
  popd
}

deploy_ae_flex_container() {
  local SCRIPT="${1:-test_flask.py}"
  build_container

  cat <<EOF > $TMP_DIR/app.yaml
  runtime: custom
  env: flex
  env_variables:
    SCRIPT: "$SCRIPT"
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
    gcloud app browse
  popd
}

deploy_gce() {
  local SCRIPT="${1:-test_flask.py}"
  build_container
  gcloud beta compute instances create-with-container \
    $(_clean_name $SCRIPT) \
    --container-image $GCR_PATH \
    --container-env SCRIPT=$SCRIPT
}


#deploy_cloudrun
#deploy_gke
#deploy_functions
#deploy_ae_standard
#deploy_ae_flex_python
#deploy_ae_flex_container
deploy_gce
