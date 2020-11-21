#!/bin/bash
set -e # exit on any failure
set -o pipefail # any step in pipe caused failure
set -u # undefined variables cause exit
set -x # verbose logs

# define variables
GCR_PATH=gcr.io/sanche-testing-project/logging:latest

# ensure the working dir is the repo root
SCRIPT_DIR=$(realpath $(dirname "$0"))
REPO_ROOT=$SCRIPT_DIR/../../..
cd $REPO_ROOT

function build_container() {
  docker build -t $GCR_PATH --file $SCRIPT_DIR/Dockerfile $REPO_ROOT
  docker push $GCR_PATH
}

function deploy_cloudrun() {
  SCRIPT="test_flask.py"
  build_container
  gcloud config set run/platform managed
  gcloud config set run/region us-west1
  gcloud run deploy  \
    --allow-unauthenticated \
    --image $GCR_PATH \
    --update-env-vars SCRIPT=$SCRIPT \
    $(echo $SCRIPT | tr -d "./_")
}

deploy_cloudrun
