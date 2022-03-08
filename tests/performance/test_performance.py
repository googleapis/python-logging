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
import time

import google.cloud.logging
from google.cloud.logging_v2.services.logging_service_v2 import LoggingServiceV2Client
from google.cloud.logging_v2.services.logging_service_v2.transports import LoggingServiceV2Transport
import google.auth.credentials
from google.cloud.logging_v2 import _gapic


class MockGRPCTransport(LoggingServiceV2Transport):
    def __init__(self, latency=0, **kwargs):
        self.latency = latency
        self._wrapped_methods = {self.write_log_entries: self.write_log_entries}

    def write_log_entries(self, *args, **kwargs):
        time.sleep(self.latency)

def _make_client(mock_network=True, use_grpc=True):
    if not mock_network:
        # use a real client
        client = google.cloud.logging.Client(_use_grpc=use_grpc)
        return client
    elif use_grpc:
        # create a mock grpc client
        mock_transport = MockGRPCTransport(latency=0)
        gapic_client = LoggingServiceV2Client(transport=mock_transport)
        handwritten_client = mock.Mock()
        api = _gapic._LoggingAPI(gapic_client, handwritten_client)
        creds = mock.Mock(spec=google.auth.credentials.Credentials)
        client = google.cloud.logging.Client(project="my-project",  credentials=creds)
        client._logging_api = api
        return client
    else:
        # create mock http client
        return None

def logger_log(num_logs=100, log_chars=10, use_grpc=True):
    client = _make_client(mock_network=True, use_grpc=use_grpc)
    logger = client.logger(name="test_logger")
    log_message = "message "
    log_message = log_message * math.ceil(log_chars / len(log_message))
    log_message = log_message[:log_chars]
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

