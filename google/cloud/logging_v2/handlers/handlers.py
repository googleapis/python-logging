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

"""Python :mod:`logging` handlers for Cloud Logging."""

import json
import logging

from google.cloud.logging_v2.logger import _GLOBAL_RESOURCE
from google.cloud.logging_v2.handlers.transports import BackgroundThreadTransport
from google.cloud.logging_v2.handlers._monitored_resources import detect_resource
from google.cloud.logging_v2.handlers._helpers import get_request_data

DEFAULT_LOGGER_NAME = "python"

"""Exclude internal logs from propagating through handlers"""
EXCLUDED_LOGGER_DEFAULTS = (
    "google.cloud",
    "google.auth",
    "google_auth_httplib2",
    "google.api_core.bidi",
    "werkzeug",
)

_CLEAR_HANDLER_RESOURCE_TYPES = ("gae_app", "cloud_function")


class CloudLoggingFilter(logging.Filter):
    """Python standard ``logging`` Filter class to add Cloud Logging
    information to each LogRecord.

    When attached to a LogHandler, each incoming log will be modified
    to include new Cloud Logging relevant data. This data can be manually
    overwritten using the `extras` argument when writing logs.
    """

    # The subset of http_request fields have been tested to work consistently across GCP environments
    # https://cloud.google.com/logging/docs/reference/v2/rest/v2/LogEntry#httprequest
    _supported_http_fields = ("requestMethod", "requestUrl", "userAgent", "protocol")

    def __init__(self, project=None, default_labels=None):
        self.project = project
        self.default_labels = default_labels if default_labels else {}

    @staticmethod
    def _infer_source_location(record):
        """Helper function to infer source location data from a LogRecord.
        Will default to record.source_location if already set
        """
        if hasattr(record, "source_location"):
            return record.source_location
        else:
            name_map = [
                ("line", "lineno"),
                ("file", "pathname"),
                ("function", "funcName"),
            ]
            output = {}
            for (gcp_name, std_lib_name) in name_map:
                value = getattr(record, std_lib_name, None)
                if value is not None:
                    output[gcp_name] = value
            return output if output else None

    def filter(self, record):
        """
        Add new Cloud Logging data to each LogRecord as it comes in
        """
        user_labels = getattr(record, "labels", {})
        # infer request data from the environment
        inferred_http, inferred_trace, inferred_span = get_request_data()
        if inferred_http is not None:
            # filter inferred_http to include only well-supported fields
            inferred_http = {
                k: v
                for (k, v) in inferred_http.items()
                if k in self._supported_http_fields and v is not None
            }
        if inferred_trace is not None and self.project is not None:
            # add full path for detected trace
            inferred_trace = f"projects/{self.project}/traces/{inferred_trace}"
        # set new record values
        record._resource = getattr(record, "resource", None)
        record._trace = getattr(record, "trace", inferred_trace) or None
        record._span_id = getattr(record, "span_id", inferred_span) or None
        record._http_request = getattr(record, "http_request", inferred_http)
        record._source_location = CloudLoggingFilter._infer_source_location(record)
        record._labels = {**self.default_labels, **user_labels} or None
        # create string representations for structured logging
        record._trace_str = record._trace or ""
        record._span_id_str = record._span_id or ""
        record._http_request_str = json.dumps(record._http_request or {})
        record._source_location_str = json.dumps(record._source_location or {})
        record._labels_str = json.dumps(record._labels or {})
        # break quotes for parsing through structured logging
        record._msg_str = str(record.msg).replace('"', '\\"') if record.msg else ""
        return True


class CloudLoggingHandler(logging.StreamHandler):
    """Handler that directly makes Cloud Logging API calls.

    This is a Python standard ``logging`` handler using that can be used to
    route Python standard logging messages directly to the Stackdriver
    Logging API.

    This handler is used when not in GAE or GKE environment.

    This handler supports both an asynchronous and synchronous transport.

    Example:

    .. code-block:: python

        import logging
        import google.cloud.logging
        from google.cloud.logging_v2.handlers import CloudLoggingHandler

        client = google.cloud.logging.Client()
        handler = CloudLoggingHandler(client)

        cloud_logger = logging.getLogger('cloudLogger')
        cloud_logger.setLevel(logging.INFO)
        cloud_logger.addHandler(handler)

        cloud_logger.error('bad news')  # API call
    """

    def __init__(
        self,
        client,
        *,
        name=DEFAULT_LOGGER_NAME,
        transport=BackgroundThreadTransport,
        resource=_GLOBAL_RESOURCE,
        labels=None,
        stream=None,
    ):
        """
        Args:
            client (~logging_v2.client.Client):
                The authenticated Google Cloud Logging client for this
                handler to use.
            name (str): the name of the custom log in Cloud Logging.
                Defaults to 'python'. The name of the Python logger will be represented
                in the ``python_logger`` field.
            transport (~logging_v2.transports.Transport):
                Class for creating new transport objects. It should
                extend from the base :class:`.Transport` type and
                implement :meth`.Transport.send`. Defaults to
                :class:`.BackgroundThreadTransport`. The other
                option is :class:`.SyncTransport`.
            resource (~logging_v2.resource.Resource):
                Resource for this Handler. Defaults to ``global``.
            labels (Optional[dict]): Additional labels to attach to logs.
            stream (Optional[IO]): Stream to be used by the handler.
        """
        super(CloudLoggingHandler, self).__init__(stream)
        self.name = name
        self.client = client
        self.transport = transport(client, name)
        self.project_id = client.project
        self.resource = resource
        self.labels = labels
        # add extra keys to log record
        log_filter = CloudLoggingFilter(project=self.project_id, default_labels=labels)
        self.addFilter(log_filter)

    def emit(self, record):
        """Actually log the specified logging record.

        Overrides the default emit behavior of ``StreamHandler``.

        See https://docs.python.org/2/library/logging.html#handler-objects

        Args:
            record (logging.LogRecord): The record to be logged.
        """
        message = super(CloudLoggingHandler, self).format(record)
        # send off request
        self.transport.send(
            record,
            message,
            resource=(record._resource or self.resource),
            labels=record._labels,
            trace=record._trace,
            span_id=record._span_id,
            http_request=record._http_request,
            source_location=record._source_location,
        )


def setup_logging(
    handler, *, excluded_loggers=EXCLUDED_LOGGER_DEFAULTS, log_level=logging.INFO
):
    """Attach a logging handler to the Python root logger

    Excludes loggers that this library itself uses to avoid
    infinite recursion.

    Example:

    .. code-block:: python

        import logging
        import google.cloud.logging
        from google.cloud.logging_v2.handlers import CloudLoggingHandler

        client = google.cloud.logging.Client()
        handler = CloudLoggingHandler(client)
        google.cloud.logging.handlers.setup_logging(handler)
        logging.getLogger().setLevel(logging.DEBUG)

        logging.error('bad news')  # API call

    Args:
        handler (logging.handler): the handler to attach to the global handler
        excluded_loggers (Optional[Tuple[str]]): The loggers to not attach the handler
            to. This will always include the loggers in the
            path of the logging client itself.
        log_level (Optional[int]): Python logging log level. Defaults to
            :const:`logging.INFO`.
    """
    all_excluded_loggers = set(excluded_loggers + EXCLUDED_LOGGER_DEFAULTS)
    logger = logging.getLogger()

    # remove built-in handlers on App Engine or Cloud Functions environments
    if detect_resource().type in _CLEAR_HANDLER_RESOURCE_TYPES:
        logger.handlers.clear()

    logger.setLevel(log_level)
    logger.addHandler(handler)
    for logger_name in all_excluded_loggers:
        # prevent excluded loggers from propagating logs to handler
        logger = logging.getLogger(logger_name)
        logger.propagate = False
