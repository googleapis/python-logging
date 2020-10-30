# Copyright 2016 Google LLC
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
#

from google.cloud.logging_v2 import __version__
from google.cloud.logging_v2 import ASCENDING
from google.cloud.logging_v2 import DESCENDING
from google.cloud.logging_v2 import client
from google.cloud.logging_v2 import entries
from google.cloud.logging_v2 import handlers
from google.cloud.logging_v2 import logger
from google.cloud.logging_v2 import metric
from google.cloud.logging_v2 import sink
from google.cloud.logging_v2 import types
from google.cloud.logging_v2.gapic import enums
from google.cloud.logging_v2 import ConfigServiceV2Client
from google.cloud.logging_v2 import LoggingServiceV2Client
from google.cloud.logging_v2 import MetricsServiceV2Client

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
