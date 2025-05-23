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
import collections
import json
import logging
import logging.handlers

import google.cloud.logging_v2
from google.cloud.logging_v2._instrumentation import _create_diagnostic_entry
from google.cloud.logging_v2.handlers.handlers import (
    CloudLoggingFilter,
    _format_and_parse_message,
)

GCP_FORMAT = (
    "{%(_payload_str)s"
    '"severity": "%(levelname)s", '
    '"logging.googleapis.com/labels": %(_labels_str)s, '
    '"logging.googleapis.com/trace": "%(_trace_str)s", '
    '"logging.googleapis.com/spanId": "%(_span_id_str)s", '
    '"logging.googleapis.com/trace_sampled": %(_trace_sampled_str)s, '
    '"logging.googleapis.com/sourceLocation": %(_source_location_str)s, '
    '"httpRequest": %(_http_request_str)s '
    "}"
)

# reserved fields taken from Structured Logging documentation:
# https://cloud.google.com/logging/docs/structured-logging
GCP_STRUCTURED_LOGGING_FIELDS = frozenset(
    {
        "severity",
        "httpRequest",
        "time",
        "timestamp",
        "timestampSeconds",
        "timestampNanos",
        "logging.googleapis.com/insertId",
        "logging.googleapis.com/labels",
        "logging.googleapis.com/operation",
        "logging.googleapis.com/sourceLocation",
        "logging.googleapis.com/spanId",
        "logging.googleapis.com/trace",
        "logging.googleapis.com/trace_sampled",
    }
)


class StructuredLogHandler(logging.StreamHandler):
    """Handler to format logs into the Cloud Logging structured log format,
    and write them to standard output
    """

    def __init__(
        self,
        *,
        labels=None,
        stream=None,
        project_id=None,
        json_encoder_cls=None,
        **kwargs
    ):
        """
        Args:
            labels (Optional[dict]): Additional labels to attach to logs.
            stream (Optional[IO]): Stream to be used by the handler.
            project (Optional[str]): Project Id associated with the logs.
            json_encoder_cls (Optional[Type[JSONEncoder]]): Custom JSON encoder. Defaults to json.JSONEncoder
        """
        super(StructuredLogHandler, self).__init__(stream=stream)
        self.project_id = project_id

        # add extra keys to log record
        log_filter = CloudLoggingFilter(project=project_id, default_labels=labels)
        self.addFilter(log_filter)

        class _Formatter(logging.Formatter):
            """Formatter to format log message without traceback"""

            def format(self, record):
                """Ignore exception info to avoid duplicating it
                https://github.com/googleapis/python-logging/issues/382
                """
                record.message = record.getMessage()
                return self.formatMessage(record)

        # make logs appear in GCP structured logging format
        self._gcp_formatter = _Formatter(GCP_FORMAT)

        self._json_encoder_cls = json_encoder_cls or json.JSONEncoder

    def format(self, record):
        """Format the message into structured log JSON.
        Args:
            record (logging.LogRecord): The log record.
        Returns:
            str: A JSON string formatted for GCP structured logging.
        """
        payload = None
        message = _format_and_parse_message(record, super(StructuredLogHandler, self))

        if isinstance(message, collections.abc.Mapping):
            # remove any special fields
            for key in list(message.keys()):
                if key in GCP_STRUCTURED_LOGGING_FIELDS:
                    del message[key]
            # if input is a dictionary, encode it as a json string
            encoded_msg = json.dumps(
                message, ensure_ascii=False, cls=self._json_encoder_cls
            )
            # all json.dumps strings should start and end with parentheses
            # strip them out to embed these fields in the larger JSON payload
            if len(encoded_msg) > 2:
                payload = encoded_msg[1:-1] + ","
        elif message:
            # properly break any formatting in string to make it json safe
            encoded_message = json.dumps(
                message, ensure_ascii=False, cls=self._json_encoder_cls
            )
            payload = '"message": {},'.format(encoded_message)

        record._payload_str = payload or ""
        # convert to GCP structured logging format
        gcp_payload = self._gcp_formatter.format(record)
        return gcp_payload

    def emit(self, record):
        if google.cloud.logging_v2._instrumentation_emitted is False:
            self.emit_instrumentation_info()
        super().emit(record)

    def emit_instrumentation_info(self):
        google.cloud.logging_v2._instrumentation_emitted = True
        diagnostic_object = _create_diagnostic_entry()
        struct_logger = logging.getLogger(__name__)
        struct_logger.addHandler(self)
        struct_logger.setLevel(logging.INFO)
        struct_logger.info(diagnostic_object.payload)
        struct_logger.handlers.clear()


class AppendLabelLoggingAdapter(logging.LoggerAdapter):
    """
    Logging adapter that allows to add required
    constant key/value to the labels part of log record.
    Example:

    .. code-block:: python

        import logging
        from google.cloud.logging_v2.handlers.structured_log import AppendLabelLoggingAdapter
        from google.cloud.logging_v2.handlers.structured_log import StructuredLogHandler
        logging.root.setLevel(logging.INFO)
        logging.root.handlers = [StructuredLogHandler()]
        first_adapter = AppendLabelLoggingAdapter(logging.root, {'a': 5, 'b': 6})
        first_adapter.info('first info')
        {
            "message": "first info",
            "severity": "INFO",
            "logging.googleapis.com/labels": {"python_logger": "root", "a": 5, "b": 6}
            [...]
        }
        # Could be stacked
        second_adapter=AppendLabelLoggingAdapter(first_adapter, {'hello': 'world'})
        second_adapter.info('second info')
        {
            "message": "second info",
            "severity": "INFO",
            "logging.googleapis.com/labels": {"python_logger": "root", "hello": "world", "a": 5, "b": 6}
            [...]
        }
    """

    def __init__(self, logger, append_labels):
        """
        Args:
            logger (~logging.Logger):
                The Logger for this adapter to use.
            append_labels (~typing.Dict[str, str]): the required data to be added to logger "labels" field.
        """
        self.append_labels = append_labels
        super().__init__(logger, None)

    def process(self, msg, kwargs):
        """
        Args:
            msg (str):
                Log message
            kwargs (dict):
                logging kwargs
        """
        extra = kwargs.get("extra", {})
        labels = extra.get("labels", {})
        for label_key, label_value in self.append_labels.items():
            labels.setdefault(label_key, label_value)
        extra["labels"] = labels
        kwargs["extra"] = extra
        return msg, kwargs
