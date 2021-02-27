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

import logging
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
_CLOUD_RUN_ENV_VARS = [_CLOUD_RUN_SERVICE_ID, _CLOUD_RUN_REVISION_ID, _CLOUD_RUN_CONFIGURATION_ID]
"""Environment variables set in Cloud Run environment."""

_FUNCTION_TARGET = "FUNCTION_TARGET"
_FUNCTION_SIGNATURE = "FUNCTION_SIGNATURE_TYPE"
_FUNCTION_NAME = "FUNCTION_NAME"
_FUNCTION_REGION = "FUNCTION_REGION"
_FUNCTION_ENTRY = "ENTRY_POINT"
_FUNCTION_ENV_VARS = [_FUNCTION_TARGET, _FUNCTION_SIGNATURE_TYPE, _CLOUD_RUN_SERVICE_ID]
_LEGACY_FUNCTION_ENV_VARS = [_FUNCTION_NAME, _FUNCTION_REGION, _FUNCTION_ENTRY]
"""Environment variables set in Cloud Functions environments."""


_REGION_ID = "instance/region"
_ZONE_ID = "instance/zone"
_GCE_INSTANCE_ID = "instance/id"
"""Attribute in metadata server for compute region and instance."""

_GKE_CLUSTER_NAME = "instance/attributes/cluster-name"
"""Attribute in metadata server when in GKE environment."""


def create_functions_resource(project):
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
            "project_id": project,
            "function_name": function_name,
            "region": region if region else "",
        },
    )
    return resource

def create_compute_resource(project):
    instance = retrieve_metadata_server(_GCE_INSTANCE_ID)
    zone = retrieve_metadata_server(_ZONE_ID)
    resource = Resource(
        type="gce_instance",
        labels={
            "project_id": project,
            "instance_id": instance if instance else "",
            "zone": zone if zone else "",
        },
    )
    return resource


def create_cloud_run_resource(project):
    region = retrieve_metadata_server(_REGION_ID)
    resource = Resource(
        type="cloud_run_revision",
        labels={
            "project_id": project,
            "service_name": os.environ.get(_CLOUD_RUN_SERVICE_ID, ""),
            "revision_name": os.environ.get(_CLOUD_RUN_REVISION_ID, ""),
            "location": region if region else "",
            "configuration_name": os.environ.get(_CLOUD_RUN_CONFIGURATION_ID, ""),
        },
    )
    return resource

def create_app_engine_resource(project):
    resource = Resource(
        type="gae_app",
        labels={
            "project_id": project,
            "module_id": os.environ.get(_GAE_SERVICE_ENV, ""),
            "version_id": os.environ.get(_GAE_VERSION_ENV, ""),
        },
    )
    return resource

def create_global_resource(project):
    resource = Resource(
        type="global",
        labels={
            "project_id": project,
        },
    )
    return resource