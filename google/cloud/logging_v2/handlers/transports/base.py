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

"""Module containing base class for logging transport."""


class Transport(object):
    """Base class for Google Cloud Logging handler transports.

    Subclasses of :class:`Transport` must have constructors that accept a
    client and name object, and must override :meth:`send`.
    """

    def send(
        self, record, message, *, resource=None, labels=None, trace=None, span_id=None
    ):
        """Transport send to be implemented by subclasses.

        Args:
            record (logging.LogRecord): Python log record that the handler was called with.
            message (str): The message from the ``LogRecord`` after being
                formatted by the associated log formatters.
            resource (Optional[google.cloud.logging_v2.resource.Resource]):
                 Monitored resource of the entry.
            labels (Optional[dict]): Mapping of labels for the entry.
        """
        raise NotImplementedError

    def flush(self):
        """Submit any pending log records.

        For blocking/sync transports, this is a no-op.
        """
