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
import collections

from google.cloud.logging_v2.entries import StructEntry
from google.cloud.logging_v2 import __version__

_DIAGNOSTIC_INFO_KEY = "logging.googleapis.com/diagnostic"
_INSTRUMENTATION_SOURCE_KEY = "instrumentation_source"
_PYTHON_LIBRARY_NAME = "python"

_LIBRARY_VERSION = __version__

_MAX_NAME_LENGTH = 14
_MAX_VERSION_LENGTH = 14
_MAX_INSTRUMENTATION_ENTRIES = 3


def _add_instrumentation(entries, **kw):
    """Validate or add instrumentation information to a list of entries

        Ensures that a single log entry with valid instrumentation info
        is in `entries`.  If instrumentation info was manually added,
        it is validated to ensure it matches this library's information.
        Otherwise, a new diagnostic entry is prepended to the list of
        entries.

    Args:
       entries (Sequence[Mapping[str, ...]]): sequence of mappings representing
            the log entry resources to log.

    Returns:
        Sequence[Mapping[str, ...]]: entries with instrumentation info validated if present
        otherwise added to beginning of list.
    """
    is_written = False
    new_entries = []
    for entry in entries:
        if is_written:
            break
        try:
            current_info = entry.payload[_DIAGNOSTIC_INFO_KEY][
                _INSTRUMENTATION_SOURCE_KEY
            ]
            entry.payload[_DIAGNOSTIC_INFO_KEY][
                _INSTRUMENTATION_SOURCE_KEY
            ] = _validate_and_update_instrumentation(current_info)
            is_written = True
        except KeyError:  # Entry does not have instrumentation info
            pass
        except AttributeError:  # Entry does not have instrumentation info
            pass
        new_entries.append(entry)

    if not is_written:
        diagnostic_entry = _create_diagnostic_entry(**kw)
        new_entries.insert(0, diagnostic_entry.to_api_repr())
    return new_entries


def _create_diagnostic_entry(name=_PYTHON_LIBRARY_NAME, version=_LIBRARY_VERSION, **kw):
    """Create a diagnostic log entry describing this library

        The diagnostic log consists of a list of library name and version objects
        that have handled a given log entry.  If this library is the originator
        of the log entry, it will look like:
        {logging.googleapis.com/diagnostic: {instrumentation_source: [{name: "python", version: "3.0.0"}]}}

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


def _truncate_string(str, max_length):
    """Truncate a string to a maximum length

    Args:
        str(str): The string to truncate
        max_length(int): The maximum length

    Returns:
        A string containing either 'str' or a truncated version of
        'str' with an asterisk at the end
    """
    if len(str) > max_length:
        return str[:max_length] + "*"
    else:
        return str


def _validate_and_update_instrumentation(existing_info=None):
    """Validate existing instrumentation info and append the final entry

        Validates that existing instrumentation info matches this
        library's info, and ensures that there are at most 3 entries
        in the instrumentation_source array (to avoid malicious log inflation).

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
            if len(info_stack) == _MAX_INSTRUMENTATION_ENTRIES:
                break
            if _is_valid(info):
                info_stack.append(
                    _get_instrumentation_source(info["name"], info["version"])
                )

    info_stack.reverse()
    return info_stack


def _get_instrumentation_source(name=_PYTHON_LIBRARY_NAME, version=_LIBRARY_VERSION):
    """Gets a JSON representation of the instrumentation_source

    Args:
        name(str): The name of this library (e.g. 'python')
        version(str) The version of this library (e.g. '3.0.0')
    Returns:
       obj: JSON object with library information
    """
    return {
        "name": _truncate_string(name, _MAX_NAME_LENGTH),
        "version": _truncate_string(version, _MAX_VERSION_LENGTH),
    }


def _is_valid(info):
    """Validates an existing instrumentation_source entry

    Args:
        info(dict): A dictionary representing the instrumentation_source entry
    Returns:
        bool: Whether the object is a valid instrumentation_source_entry
    """
    try:
        if info["name"][: len(_PYTHON_LIBRARY_NAME)] != _PYTHON_LIBRARY_NAME:
            return False
    except KeyError:
        return False

    return True
