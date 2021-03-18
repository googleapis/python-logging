# Copyright 2021 Google LLC All Rights Reserved.
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

"""Logging handler for printing formatted structured logs to standard output.
"""

import math
import json

import logging.handlers

from google.cloud.logging_v2.handlers._helpers import format_stackdriver_json
from google.cloud.logging_v2.handlers._helpers import get_request_data

GCP_FORMAT = '{"message": "%(message)s", "severity": "%(levelname)s", "logging.googleapis.com/trace": "%(trace)s", "logging.googleapis.com/sourceLocation": { "file": "%(filename)s", "line": "%(lineno)d", "function": "%(funcName)s"}, "httpRequest": {"requestMethod": "%(request_method)s", "requestUrl": "%(request_url)s", "userAgent": "%(user_agent)s", "protocol": "%(protocol)s"} }'


class GCPFilter(logging.Filter):

    def __init(self, project=None):
        self.project = project

    def filter(self, record):
        inferred_http, inferred_trace = get_request_data()
        if inferred_trace is not None and self.project is not None:
            inferred_trace = f"projects/{self.project_id}/traces/{inferred_trace}"

        record.trace = trace_id = record.trace or inferred_trace or ""
        record.http_request = record.http_request or record.httpRequest or inferred_http or {}
        record.request_method = record.http_request.get('requestMethod', "")
        record.request_url = record.http_request.get('requestUrl', "")
        record.user_agent = record.http_request.get('userAgent', "")
        record.protocol = record.http_request.get('protocol', "")
        return True

class StructuredLogHandler(logging.StreamHandler):
    """Handler to format logs into the Cloud Logging structured log format,
    and write them to standard output
    """

    def __init__(self, *, name=None, stream=None, project=None):
        """
        Args:
            name (Optional[str]): The name of the custom log in Cloud Logging.
            stream (Optional[IO]): Stream to be used by the handler.
        """
        super(StructuredLogHandler, self).__init__(stream=stream)
        self.name = name
        self.project_id = project

        # add extra keys to log record
        self.addFilter(GCPFilter())

        # make logs appear in GCP structured logging format
        self.formatter = logging.Formatter(GCP_FORMAT)

    def format(self, record):
        """Format the message into structured log JSON.
        Args:
            record (logging.LogRecord): The log record.
        Returns:
            str: A JSON string formatted for GKE fluentd.
        """

        payload = self.formatter.format(record)
        return payload
