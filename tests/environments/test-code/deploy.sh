#!/bin/bash
set -e # exit on any failure
set -o pipefail # any step in pipe caused failure
set -u # undefined variables cause exit

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

add_service_accounts() {
  set +e
  # clour run
  PROJECT_NUMBER=$(gcloud projects list --filter=sanche-testing-project --format="value(PROJECT_NUMBER)")
  gcloud projects add-iam-policy-binding sanche-testing-project \
    --member=serviceAccount:service-$PROJECT_NUMBER@gcp-sa-pubsub.iam.gserviceaccount.com \
     --role=roles/iam.serviceAccountTokenCreator
  gcloud iam service-accounts create pubsub-invoker \
     --display-name "Pub/Sub Invoker"
  gcloud run services add-iam-policy-binding  $(_clean_name $SCRIPT) \
     --member=serviceAccount:pubsub-invoker@sanche-testing-project.iam.gserviceaccount.com \
     --role=roles/run.invoker
  RUN_URL=$(gcloud run services list --filter=router --format="value(URL)")
  gcloud pubsub subscriptions create cloudrun-subscriber --topic logging-test \
    --push-endpoint=$RUN_URL \
    --push-auth-service-account=pubsub-invoker@sanche-testing-project.iam.gserviceaccount.com
  set -e
}

######################################
# deployment functions
######################################

deploy_cloudrun() {
  local SCRIPT="${1:-router.py}"
  build_container
  gcloud config set run/platform managed
  gcloud config set run/region us-west1
  gcloud run deploy  \
    --allow-unauthenticated \
    --image $GCR_PATH \
    --update-env-vars SCRIPT=$SCRIPT \
    --update-env-vars ENABLE_FLASK=true \
    $(_clean_name $SCRIPT)
  # create pubsub subscription
  add_service_accounts
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

deploy_gke() {
  local SCRIPT="${1:-router.py}"

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

deploy_functions() {
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
    gcloud functions deploy $(_clean_name $SCRIPT) \
      --entry-point pubsub_gcf \
      --trigger-topic logging-test \
      --runtime $RUNTIME \
      --region us-west2
  popd
}

deploy_ae_standard() {
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
  # build app.yaml
  cat <<EOF > $TMP_DIR/app.yaml
    runtime: $RUNTIME
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

deploy_ae_flex_python() {
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

deploy_ae_flex_container() {
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

deploy_gce() {
  local SCRIPT="${1:-router.py}"
  build_container
  gcloud beta compute instances create-with-container \
    $(_clean_name $SCRIPT) \
    --container-image $GCR_PATH \
    --container-env SCRIPT=$SCRIPT,ENABLE_SUBSCRIBER="true"
}

######################################
# user input functions
######################################

deploy_selected() {
  case $(echo $GCP_ENV | tr -d -) in
    cloudrun | run | cr)
      deploy_cloudrun
      ;;
    kubernetes | gke | kubernetesengine)
      deploy_gke
      ;;
    functions | function | gcf | cloudfunctions)
      deploy_functions
      ;;
    compute | computeengine | gce)
      deploy_gce
      ;;
    appengine | gae | appenginestandard | gaestandard)
      deploy_ae_standard
      ;;
    gaeflex | appengineflex | gaeflexpython | appengineflexpython)
      deploy_ae_flex_python
      ;;
    gaeflexcontainer | appengineflexcontainer)
      deploy_ae_flex_container
      ;;
    *)
      echo "environment not recognized"
      exit 1
  esac
}

# parse inputs
PARAMS=""
while (( "$#" )); do
  case "$1" in
    -e|--env|--environment)
      if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
        GCP_ENV=$2
        shift 2
      else
        echo "Error: Argument for $1 is missing" >&2
        exit 1
      fi
      ;;
    -v|--verbose)
      set -x # verbose logs
      shift
      ;;
    -*|--*=) # unsupported flags
      echo "Error: Unsupported flag $1" >&2
      exit 1
      ;;
    *) # preserve positional arguments
      PARAMS="$PARAMS $1"
      shift
      ;;
  esac
done
# set positional arguments in their proper place
eval set -- "$PARAMS"

deploy_selected
