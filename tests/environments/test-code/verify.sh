#!/bin/bash
set -e # exit on any failure
set -o pipefail # any step in pipe caused failure
set -u # undefined variables cause exit

verify_gce() {
  STATUS=$(gcloud compute instances list --filter router --format="value(STATUS)")
   if [[ $STATUS == $"RUNNING" ]]; then
     echo "TRUE"
     exit 0
   else
     echo "FALSE"
     exit 1
  fi
}


######################################
# user input functions
######################################

verify_selected() {
  case $(echo $GCP_ENV | tr -d -) in
    cloudrun | run | cr)
      verify_cloudrun
      ;;
    kubernetes | gke | kubernetesengine)
      verify_gke
      ;;
    functions | function | gcf | cloudfunctions)
      verify_functions
      ;;
    compute | computeengine | gce)
      verify_gce
      ;;
    appengine | gae | appenginestandard | gaestandard)
      verify_ae_standard
      ;;
    gaeflex | appengineflex | gaeflexpython | appengineflexpython)
      verify_ae_flex_python
      ;;
    gaeflexcontainer | appengineflexcontainer)
      verify_ae_flex_container
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

verify_selected
