# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from google.cloud.logging_v2.resource import Resource
from google.cloud.logging_v2._helpers import retrieve_metadata_server

_GAE_SERVICE_ENV = "GAE_SERVICE"
_GAE_VERSION_ENV = "GAE_VERSION"
_GAE_INSTANCE_ENV = "GAE_INSTANCE"
_GAE_ENV_VARS = [_GAE_SERVICE_ENV, _GAE_VERSION_ENV, _GAE_INSTANCE_ENV]
"""Environment variables set in App Engine environment."""

_CLOUD_RUN_SERVICE_ID = "K_SERVICE"
_CLOUD_RUN_REVISION_ID = "K_REVISION"
_CLOUD_RUN_CONFIGURATION_ID = "K_CONFIGURATION"
_CLOUD_RUN_ENV_VARS = [
    _CLOUD_RUN_SERVICE_ID,
    _CLOUD_RUN_REVISION_ID,
    _CLOUD_RUN_CONFIGURATION_ID,
]
"""Environment variables set in Cloud Run environment."""

_FUNCTION_TARGET = "FUNCTION_TARGET"
_FUNCTION_SIGNATURE = "FUNCTION_SIGNATURE_TYPE"
_FUNCTION_NAME = "FUNCTION_NAME"
_FUNCTION_REGION = "FUNCTION_REGION"
_FUNCTION_ENTRY = "ENTRY_POINT"
_FUNCTION_ENV_VARS = [_FUNCTION_TARGET, _FUNCTION_SIGNATURE, _CLOUD_RUN_SERVICE_ID]
_LEGACY_FUNCTION_ENV_VARS = [_FUNCTION_NAME, _FUNCTION_REGION, _FUNCTION_ENTRY]
"""Environment variables set in Cloud Functions environments."""


_REGION_ID = "instance/region"
_ZONE_ID = "instance/zone"
_GCE_INSTANCE_ID = "instance/id"
"""Attribute in metadata server for compute region and instance."""

_GKE_CLUSTER_NAME = "instance/attributes/cluster-name"
"""Attribute in metadata server when in GKE environment."""

_PROJECT_NAME = "project/project-id"
"""Attribute in metadata server when in GKE environment."""


def _create_functions_resource():
    """Create a standardized Cloud Functions resource.
    Returns:
        google.cloud.logging.Resource
    """
    project = retrieve_metadata_server(_PROJECT_NAME)
    region = retrieve_metadata_server(_REGION_ID)
    if _FUNCTION_NAME in os.environ:
        function_name = os.environ.get(_FUNCTION_NAME)
    elif _CLOUD_RUN_SERVICE_ID in os.environ:
        function_name = os.environ.get(_CLOUD_RUN_SERVICE_ID)
    else:
        function_name = ""
    resource = Resource(
        type="cloud_function",
        labels={
            "project_id": project if project else "",
            "function_name": function_name if function_name else "",
            "region": region.split("/")[-1] if region else "",
        },
    )
    return resource


def _create_kubernetes_resource():
    """Create a standardized Kubernetes resource.
    Returns:
        google.cloud.logging.Resource
    """
    zone = retrieve_metadata_server(_ZONE_ID)
    cluster_name = retrieve_metadata_server(_GKE_CLUSTER_NAME)
    project = retrieve_metadata_server(_PROJECT_NAME)

    resource = Resource(
        type="k8s_container",
        labels={
            "project_id": project if project else "",
            "location": zone if zone else "",
            "cluster_name": cluster_name if cluster_name else "",
        },
    )
    return resource


def _create_compute_resource():
    """Create a standardized Compute Engine resource.
    Returns:
        google.cloud.logging.Resource
    """
    instance = retrieve_metadata_server(_GCE_INSTANCE_ID)
    zone = retrieve_metadata_server(_ZONE_ID)
    project = retrieve_metadata_server(_PROJECT_NAME)
    resource = Resource(
        type="gce_instance",
        labels={
            "project_id": project if project else "",
            "instance_id": instance if instance else "",
            "zone": zone if zone else "",
        },
    )
    return resource


def _create_cloud_run_resource():
    """Create a standardized Cloud Run resource.
    Returns:
        google.cloud.logging.Resource
    """
    region = retrieve_metadata_server(_REGION_ID)
    project = retrieve_metadata_server(_PROJECT_NAME)
    resource = Resource(
        type="cloud_run_revision",
        labels={
            "project_id": project if project else "",
            "service_name": os.environ.get(_CLOUD_RUN_SERVICE_ID, ""),
            "revision_name": os.environ.get(_CLOUD_RUN_REVISION_ID, ""),
            "location": region.split("/")[-1] if region else "",
            "configuration_name": os.environ.get(_CLOUD_RUN_CONFIGURATION_ID, ""),
        },
    )
    return resource


def _create_app_engine_resource():
    """Create a standardized App Engine resource.
    Returns:
        google.cloud.logging.Resource
    """
    zone = retrieve_metadata_server(_ZONE_ID)
    project = retrieve_metadata_server(_PROJECT_NAME)
    resource = Resource(
        type="gae_app",
        labels={
            "project_id": project if project else "",
            "module_id": os.environ.get(_GAE_SERVICE_ENV, ""),
            "version_id": os.environ.get(_GAE_VERSION_ENV, ""),
            "zone": zone if zone else "",
        },
    )
    return resource


def _create_global_resource(project):
    """Create a global resource.
    Args:
        project (str): The project ID to pass on to the resource
    Returns:
        google.cloud.logging.Resource
    """
    return Resource(type="global", labels={"project_id": project if project else ""})


def detect_resource(project=""):
    """Return the default monitored resource based on the local environment.
    If GCP resource not found, defaults to `global`.

    Args:
        project (str): The project ID to pass on to the resource (if needed)
    Returns:
        google.cloud.logging.Resource: The default resource based on the environment
    """
    gke_cluster_name = retrieve_metadata_server(_GKE_CLUSTER_NAME)
    gce_instance_name = retrieve_metadata_server(_GCE_INSTANCE_ID)

    if all([env in os.environ for env in _GAE_ENV_VARS]):
        # App Engine Flex or Standard
        return _create_app_engine_resource()
    elif gke_cluster_name is not None:
        # Kubernetes Engine
        return _create_kubernetes_resource()
    elif all([env in os.environ for env in _LEGACY_FUNCTION_ENV_VARS]) or all(
        [env in os.environ for env in _FUNCTION_ENV_VARS]
    ):
        # Cloud Functions
        return _create_functions_resource()
    elif all([env in os.environ for env in _CLOUD_RUN_ENV_VARS]):
        # Cloud Run
        return _create_cloud_run_resource()
    elif gce_instance_name is not None:
        # Compute Engine
        return _create_compute_resource()
    else:
        # use generic global resource
        return _create_global_resource(project)
