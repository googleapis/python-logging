# Copyright 2022 Google LLC
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

"""Add diagnostic instrumentation source information to logs"""

from google.cloud.logging_v2.entries import StructEntry

_DIAGNOSTIC_INFO_KEY = "logging.googleapis.com/diagnostic"
_INSTRUMENTATION_SOURCE_KEY = "instrumentation_source"
_PYTHON_LIBRARY_NAME = "python"

_LIBRARY_VERSION = "3.0.0"

def create_diagnostic_entry(library_name=None, library_version=None):
    """Create a diagnostic log entry describing this library

    Args:
        library_name(str): The name of this library (e.g. 'python')
        library_version(str) The version of this library (e.g. '3.0.0')
    
    Returns:
        google.cloud.logging.entries.LogEntry: Log entry with library information
    """
    payload = {_DIAGNOSTIC_INFO_KEY: {
        _INSTRUMENTATION_SOURCE_KEY: {
            "name": _PYTHON_LIBRARY_NAME,
            "version": _LIBRARY_VERSION,
        }
    }}
    entry = StructEntry(payload=payload)
    return entry