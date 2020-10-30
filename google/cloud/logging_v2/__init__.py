# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import pkg_resources

try:
    __version__ = pkg_resources.get_distribution("google-cloud-logging").version
except pkg_resources.DistributionNotFound:
    __version__ = None


from google.cloud.logging_v2 import client
from google.cloud.logging_v2 import entries
from google.cloud.logging_v2 import handlers
from google.cloud.logging_v2 import logger
from google.cloud.logging_v2 import metric
from google.cloud.logging_v2 import sink
from google.cloud.logging_v2 import types
from google.cloud.logging_v2.gapic import enums
from google.cloud.logging_v2.gapic import config_service_v2_client
from google.cloud.logging_v2.gapic import logging_service_v2_client
from google.cloud.logging_v2.gapic import metrics_service_v2_client



ASCENDING = "timestamp asc"
"""Query string to order by ascending timestamps."""
DESCENDING = "timestamp desc"
"""Query string to order by decending timestamps."""


class LoggingServiceV2Client(logging_service_v2_client.LoggingServiceV2Client):
    __doc__ = logging_service_v2_client.LoggingServiceV2Client.__doc__
    enums = enums


class ConfigServiceV2Client(config_service_v2_client.ConfigServiceV2Client):
    __doc__ = config_service_v2_client.ConfigServiceV2Client.__doc__
    enums = enums


class MetricsServiceV2Client(metrics_service_v2_client.MetricsServiceV2Client):
    __doc__ = metrics_service_v2_client.MetricsServiceV2Client.__doc__
    enums = enums


__all__ = (
    "__version__",
    "ASCENDING",
    "client",
    "ConfigServiceV2Client",
    "DESCENDING",
    "enums",
    "handlers",
    "logger",
    "LoggingServiceV2Client",
    "metric",
    "MetricsServiceV2Client",
    "sink",
    "types",
)
