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

import unittest
from datetime import datetime


class TestStructuredLogHandler(unittest.TestCase):
    PROJECT = "PROJECT"

    def _get_target_class(self):
        from google.cloud.logging.handlers import StructuredLogHandler

        return StructuredLogHandler

    def _make_one(self, *args, **kw):
        return self._get_target_class()(*args, **kw)

    def test_ctor_defaults(self):
        handler = self._make_one()
        self.assertIsNone(handler.name)

    def test_ctor_w_name(self):
        handler = self._make_one(name="foo")
        self.assertEqual(handler.name, "foo")

    def test_format(self):
        import logging
        import json

        handler = self._make_one()
        logname = "loggername"
        message = "hello world，嗨 世界"
        pathname = "testpath"
        lineno = 1
        func = "test-function"
        record = logging.LogRecord(
            logname, logging.INFO, pathname, lineno, message, None, None, func=func
        )
        record.created = 5.03
        iso_timestamp = datetime.fromtimestamp(record.created).isoformat() + "Z"
        expected_payload = {
            "message": message,
            "timestamp": iso_timestamp,
            "severity": record.levelname,
            "logging.googleapis.com/sourceLocation": {
                "file": pathname,
                "line": str(lineno),
                "function": func
            }
        }
        handler.filter(record)
        payload = handler.format(record)
        result =  json.loads(handler.format(record))
        for (key, value) in expected_payload.items():
            self.assertEqual(value, result[key])
