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
from google.cloud.logging_v2 import __version__

_DIAGNOSTIC_INFO_KEY = "logging.googleapis.com/diagnostic"
_INSTRUMENTATION_SOURCE_KEY = "instrumentation_source"
_PYTHON_LIBRARY_NAME = "python"

_LIBRARY_VERSION = __version__

_MAX_NAME_LENGTH = 14
_MAX_VERSION_LENGTH = 16

def create_diagnostic_entry(name=None, version=None):
    """Create a diagnostic log entry describing this library

    Args:
        name(str): The name of this library (e.g. 'python')
        version(str) The version of this library (e.g. '3.0.0')
    
    Returns:
        google.cloud.logging.entries.LogEntry: Log entry with library information
    """
    name = name if name != None else _PYTHON_LIBRARY_NAME
    version = version if version != None else _LIBRARY_VERSION
    payload = {_DIAGNOSTIC_INFO_KEY: {
        _INSTRUMENTATION_SOURCE_KEY: {
            "name": truncate_string(name, _MAX_NAME_LENGTH),
            "version": truncate_string(version, 16),
        }
    }}
    entry = StructEntry(payload=payload)
    return entry

def truncate_string(str, max_length):
    """Truncate a string to a maximum length

    Args:
        str(str): The string to truncate
        max_length(int): The maximum length

    Returns:
        A string containing either 'str' or a truncated version of 
        'str' with an asterisk at the end
    """
    if len(str) > max_length:
        return str[:max_length-1] + "*"
    else: return str