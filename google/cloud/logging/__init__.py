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

from google.cloud.logging_v2.client import Client
from google.cloud.logging_v2.entries import LogEntry
from google.cloud.logging_v2.entries import TextEntry
from google.cloud.logging_v2.entries import ProtobufEntry
from google.cloud.logging_v2.entries import StructEntry
from google.cloud.logging_v2.logger import Logger
from google.cloud.logging_v2.logger import Batch
from google.cloud.logging_v2.metric import Metric
from google.cloud.logging_v2.sink import Sink
from google.cloud.logging_v2 import handlers
from google.cloud.logging_v2 import __version__ as version


__all__ = (
    "Client",
    "LogEntry",
    "TextEntry",
    "ProtobufEntry",
    "StructEntry",
    "Logger",
    "Batch",
    "Metric",
    "Sink",
    "handlers",
)

__version__ = version
