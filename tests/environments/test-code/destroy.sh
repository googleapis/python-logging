#!/bin/bash
set -e # exit on any failure
set -o pipefail # any step in pipe caused failure
set -u # undefined variables cause exit

destroy_gce() {
  gcloud compute instances delete router -q
}


######################################
# user input functions
######################################

destroy_selected() {
  case $(echo $GCP_ENV | tr -d -) in
    cloudrun | run | cr)
      destroy_cloudrun
      ;;
    kubernetes | gke | kubernetesengine)
      destroy_gke
      ;;
    functions | function | gcf | cloudfunctions)
      destroy_functions
      ;;
    compute | computeengine | gce)
      destroy_gce
      ;;
    appengine | gae | appenginestandard | gaestandard)
      destroy_ae_standard
      ;;
    gaeflex | appengineflex | gaeflexpython | appengineflexpython)
      destroy_ae_flex_python
      ;;
    gaeflexcontainer | appengineflexcontainer)
      destroy_ae_flex_container
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

destroy_selected
