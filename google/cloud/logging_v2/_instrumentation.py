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
_MAX_VERSION_LENGTH = 14


def add_instrumentation(entries, **kw):
    """Validate or add instrumentation information to a list of entries

    Args:
       entries (Sequence[Mapping[str, ...]]): sequence of mappings representing
            the log entry resources to log.

    Returns:
        Sequence[Mapping[str, ...]]: entries with instrumentation info validated if present
        otherwise added to beginning of list.
    """
    is_written = False
    for entry in entries:
        if (
            is_written is False
            and hasattr(entry, "payload")
            and entry.payload is dict
            and _DIAGNOSTIC_INFO_KEY in entry.payload
            and _INSTRUMENTATION_SOURCE_KEY in entry.payload[_DIAGNOSTIC_INFO_KEY]
        ):
            current_info = entry.payload[_DIAGNOSTIC_INFO_KEY][
                _INSTRUMENTATION_SOURCE_KEY
            ]
            entry.payload[_DIAGNOSTIC_INFO_KEY][
                _INSTRUMENTATION_SOURCE_KEY
            ] = validate_and_update_instrumentation(current_info)
            is_written = True
        else:
            diagnostic_entry = create_diagnostic_entry(**kw)
            entries.insert(0, diagnostic_entry.to_api_repr())
        return entries


def create_diagnostic_entry(name=None, version=None, **kw):
    """Create a diagnostic log entry describing this library

    Args:
        name(str): The name of this library (e.g. 'python')
        version(str) The version of this library (e.g. '3.0.0')

    Returns:
        google.cloud.logging_v2.LogEntry: Log entry with library information
    """
    payload = {
        _DIAGNOSTIC_INFO_KEY: {
            _INSTRUMENTATION_SOURCE_KEY: [_get_instrumentation_source(name, version)]
        }
    }
    kw["severity"] = "INFO"
    entry = StructEntry(payload=payload, **kw)
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
        return str[: max_length ] + "*"
    else:
        return str


def validate_and_update_instrumentation(existing_info=None):
    """Validate existing instrumentation info and append the final entry

    Args:
        existing_info: A list of instrumentation_source objects already on an etnry

    Returns:
        A validated list of instrumentation_source objects with the current
        library entry at the end
    """
    info_stack = []
    info_stack.append(_get_instrumentation_source())
    if existing_info:
        for info in existing_info[::-1]:
            if len(info_stack) == 3:
                break
            if _is_valid(info):
                info_stack.append(
                    _get_instrumentation_source(info["name"], info["version"])
                )

    info_stack.reverse()
    return info_stack


def _get_instrumentation_source(name=None, version=None):
    """Gets a JSON representation of the instrumentation_source

    Args:
        name(str): The name of this library (e.g. 'python')
        version(str) The version of this library (e.g. '3.0.0')
    Returns:
       obj: JSON object with library information
    """
    name = name if name is not None else _PYTHON_LIBRARY_NAME
    version = version if version is not None else _LIBRARY_VERSION
    return {
        "name": truncate_string(name, _MAX_NAME_LENGTH),
        "version": truncate_string(version, _MAX_VERSION_LENGTH),
    }


def _is_valid(info):
    """Validates an existing instrumentation_source entry

    Args:
        info(dict): A dictionary representing the instrumentation_source entry
    Returns:
        bool: Whether the object is a valid instrumentation_source_entry
    """
    if "name" not in info:
        return False
    if "version" not in info:
        return False
    if info["name"][: len(_PYTHON_LIBRARY_NAME)] != _PYTHON_LIBRARY_NAME:
        return False
    return True
