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

import logging
import unittest


class TestSyncHandler(unittest.TestCase):

    PROJECT = "PROJECT"

    @staticmethod
    def _get_target_class():
        from google.cloud.logging_v2.handlers.transports import SyncTransport

        return SyncTransport

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor(self):
        client = _Client(self.PROJECT)
        NAME = "python_logger"
        transport = self._make_one(client, NAME)
        self.assertEqual(transport.logger.name, "python_logger")

    def test_send(self):
        from google.cloud.logging_v2.logger import _GLOBAL_RESOURCE
        from google.cloud.logging_v2._helpers import LogSeverity

        client = _Client(self.PROJECT)

        stackdriver_logger_name = "python"
        python_logger_name = "mylogger"
        transport = self._make_one(client, stackdriver_logger_name)
        message = "hello world"
        record = logging.LogRecord(
            python_logger_name, logging.INFO, None, None, message, None, None
        )

        transport.send(record, message, resource=_GLOBAL_RESOURCE)
        EXPECTED_STRUCT = {"message": message, "python_logger": python_logger_name}
        EXPECTED_SENT = (
            EXPECTED_STRUCT,
            LogSeverity.INFO,
            _GLOBAL_RESOURCE,
            None,
            None,
            None,
        )
        self.assertEqual(transport.logger.log_struct_called_with, EXPECTED_SENT)


class _Logger(object):
    from google.cloud.logging_v2.logger import _GLOBAL_RESOURCE

    def __init__(self, name):
        self.name = name

    def log_struct(
        self,
        message,
        severity=None,
        resource=_GLOBAL_RESOURCE,
        labels=None,
        trace=None,
        span_id=None,
    ):
        self.log_struct_called_with = (
            message,
            severity,
            resource,
            labels,
            trace,
            span_id,
        )


class _Client(object):
    def __init__(self, project):
        self.project = project

    def logger(self, name):  # pylint: disable=unused-argument
        self._logger = _Logger(name)
        return self._logger


class _Handler(object):
    def __init__(self, level):
        self.level = level  # pragma: NO COVER

    def acquire(self):
        pass  # pragma: NO COVER

    def release(self):
        pass  # pragma: NO COVER
