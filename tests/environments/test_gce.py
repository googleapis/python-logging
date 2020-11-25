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

import datetime
import logging
import unittest

from google.api_core.exceptions import BadGateway
from google.api_core.exceptions import Conflict
from google.api_core.exceptions import NotFound
from google.api_core.exceptions import TooManyRequests
from google.api_core.exceptions import ResourceExhausted
from google.api_core.exceptions import RetryError
from google.api_core.exceptions import ServiceUnavailable
import google.cloud.logging
from google.cloud._helpers import UTC
from google.cloud.logging_v2.handlers.handlers import CloudLoggingHandler
from google.cloud.logging_v2.handlers.transports import SyncTransport
from google.cloud.logging_v2 import client
from google.cloud.logging_v2.resource import Resource

from test_utils.retry import RetryErrors
from test_utils.retry import RetryResult
from test_utils.system import unique_resource_id


class TestGKE(unittest.TestCase):


    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_test(self):
        self.assertTrue(True)
