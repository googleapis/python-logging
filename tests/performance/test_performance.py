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
import pytest
import unittest
import math
import mock

import google.cloud.logging
from google.cloud.logging_v2.services.logging_service_v2 import LoggingServiceV2Client
import google.auth.credentials
from google.cloud.logging_v2 import _gapic


def _make_client():
    creds = mock.Mock(spec=google.auth.credentials.Credentials)
    gapic_client = LoggingServiceV2Client(credentials=creds)
    handwritten_client = mock.Mock()
    api = _gapic._LoggingAPI(gapic_client, handwritten_client)
    client = google.cloud.logging.Client(project="my-project",  credentials=creds)
    client._logging_api = api
    return client

def logger_log(num_logs=100, log_chars=10, use_grpc=True):
    # client = google.cloud.logging.Client(project="my-project",  credentials=_make_credentials(), _use_grpc=use_grpc)
    client = _make_client()
    logger = client.logger(name="test_logger")
    log_message = "message "
    log_message = log_message * math.ceil(log_chars / len(log_message))
    log_message = log_message[:log_chars]
    with mock.patch.object(
        type(client._logging_api._gapic_api.transport.write_log_entries), "__call__"
    ) as call:
        call.return_value = None
        for i in range(num_logs):
            logger.log(log_message)
            print(log_message)

class TestPerformance(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_test(self):
        logger_log()
        self.assertIsNone(None)

