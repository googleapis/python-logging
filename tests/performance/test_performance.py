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
import itertools

import pandas as pd
from tqdm import tqdm

import google.cloud.logging
from google.cloud.logging_v2.services.logging_service_v2 import LoggingServiceV2Client
from google.cloud.logging_v2.services.logging_service_v2.transports import LoggingServiceV2Transport
from google.cloud.logging_v2._http import _LoggingAPI
import google.auth.credentials
from google.cloud.logging_v2 import _gapic


class MockGRPCTransport(LoggingServiceV2Transport):
    """
    Mock for grpc transport.
    Instead of sending logs to server, introduce artificial delay
    """
    def __init__(self, latency=0, **kwargs):
        self.latency = latency
        self._wrapped_methods = {self.write_log_entries: self.write_log_entries}

    def write_log_entries(self, *args, **kwargs):
        time.sleep(self.latency)

class MockHttpAPI(_LoggingAPI):
    """
    Mock for http API implementation.
    Instead of sending logs to server, introduce artificial delay
    """
    def __init__(self, client, latency=0):
        self._client = client
        self.api_request = lambda **kwargs: time.sleep(latency)

def _make_client(mock_network=True, use_grpc=True, mock_latency=0.01):
    """
    Create and return a new test client to manage writing logs
    Can optionally create a real GCP client, or a mock client with artificial network calls
    Can choose between grpc and http client implementations
    """
    if not mock_network:
        # use a real client
        client = google.cloud.logging.Client(_use_grpc=use_grpc)
        return client
    elif use_grpc:
        # create a mock grpc client
        mock_transport = MockGRPCTransport(latency=mock_latency)
        gapic_client = LoggingServiceV2Client(transport=mock_transport)
        handwritten_client = mock.Mock()
        api = _gapic._LoggingAPI(gapic_client, handwritten_client)
        creds = mock.Mock(spec=google.auth.credentials.Credentials)
        client = google.cloud.logging.Client(project="my-project",  credentials=creds)
        client._logging_api = api
        return client
    else:
        # create a mock http client
        creds = mock.Mock(spec=google.auth.credentials.Credentials)
        client = google.cloud.logging.Client(project="my-project",  credentials=creds)
        mock_http = MockHttpAPI(client, latency=mock_latency)
        client._logging_api = mock_http
        return client

def logger_log(client, num_logs=100, payload_size=10, json_payload=False):
    # build pay load
    log_payload = "message "
    log_payload = log_payload * math.ceil(payload_size / len(log_payload))
    log_payload = log_payload[:payload_size]
    if json_payload:
        log_payload = {"key": log_payload}
    # start code under test
    start = time.perf_counter()
    # build logger
    logger = client.logger(name="test_logger")
    # create logs
    for i in range(num_logs):
        logger.log(log_payload)
    end = time.perf_counter()
    return end - start

def batch_log(client, num_logs=100, payload_size=10, json_payload=False):
    # build pay load
    log_payload = "message "
    log_payload = log_payload * math.ceil(payload_size / len(log_payload))
    log_payload = log_payload[:payload_size]
    if json_payload:
        log_payload = {"key": log_payload}
    # start code under test
    start = time.perf_counter()
    # build logger
    logger = client.logger(name="test_logger")
    # create logs
    with logger.batch() as batch:
        for i in range(num_logs):
            batch.log(log_payload)
    end = time.perf_counter()
    return end - start

def benchmark():
    results = []
    # api, use_grpc, json_payload, payload_size
    tests = list(itertools.product(['logger.log', 'batch.log'], [True, False], [True, False], [10, 10000]))
    with tqdm(total=len(tests)) as pbar:
        for api, use_grpc, json_payload, payload_size in tests:
            num_logs = 100
            client = _make_client(mock_network=True, use_grpc=use_grpc)
            if api == 'logger.log':
                time = logger_log(client, num_logs=num_logs, payload_size=payload_size, json_payload=json_payload)
            elif api == 'batch.log':
                time = batch_log(client, num_logs=num_logs, payload_size=payload_size, json_payload=json_payload)
            else:
                raise RuntimeError(f"Unknownapi: {api}")
            network_str = "grpc" if use_grpc else "http"
            payload_str = "json" if json_payload else "text"
            size_str = "small" if payload_size < 100 else "large"
            result = {"API": api, "network": network_str, "payload_type": payload_str, "payload_size": size_str, "exec_time":time}
            results.append(result)
            pbar.update()
    benchmark_df = pd.DataFrame(results)
    print(benchmark_df.to_string(index=False))

class TestPerformance(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        print("Done")


    def test_benchmark(self):
        benchmark()

    # def test_test(self):

    #     client = _make_client(mock_network=True, use_grpc=False, mock_latency=0)
    #     logger_log(client)

