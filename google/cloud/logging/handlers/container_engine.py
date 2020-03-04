# Copyright 2016 Google LLC All Rights Reserved.
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

"""Logging handler for Google Container Engine (GKE).

Formats log messages in a JSON format, so that Kubernetes clusters with the
fluentd Google Cloud plugin installed can format their log messages so that
metadata such as log level is properly captured.
"""

import logging.handlers

from google.cloud.logging.handlers._helpers import format_stackdriver_json, get_trace_id
from google.cloud.logging._helpers import retrieve_metadata_server

_TRACE_ID_LABEL = "logging.googleapis.com/trace"
_PROJECT_ID = "project/project-id"
"""Attribute in metadata server for the current project-id."""


class ContainerEngineHandler(logging.StreamHandler):
    """Handler to format log messages the format expected by GKE fluent.

    This handler is written to format messages for the Google Container Engine
    (GKE) fluentd plugin, so that metadata such as log level are properly set.

    :type name: str
    :param name: (optional) the name of the custom log in Stackdriver Logging.

    :type stream: file-like object
    :param stream: (optional) stream to be used by the handler.
    """

    def __init__(self, name=None, stream=None):
        super(ContainerEngineHandler, self).__init__(stream=stream)
        self.name = name

        self.project_id = retrieve_metadata_server(_PROJECT_ID)

    def get_gke_labels(self):
        """Return the labels for GKE app.

        If the trace ID can be detected, it will be included as a label.
        Currently, no other labels are included.

        :rtype: dict
        :returns: Labels for GKE app.
        """
        gke_labels = {}

        trace_id = get_trace_id()
        if trace_id is not None:
            gke_labels[_TRACE_ID_LABEL] = "projects/{}/traces/{}".format(
                self.project_id, trace_id
            )

        return gke_labels

    def format(self, record):
        """Format the message into JSON expected by fluentd.

        :type record: :class:`~logging.LogRecord`
        :param record: the log record

        :rtype: str
        :returns: A JSON string formatted for GKE fluentd.
        """
        message = super(ContainerEngineHandler, self).format(record)
        gke_labels = self.get_gke_labels()
        return format_stackdriver_json(record, message, **gke_labels)
