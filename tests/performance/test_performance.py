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
import io
import logging
from pathlib import Path

import pandas as pd
from tqdm import tqdm
import cProfile
import pstats
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
import rich

import google.cloud.logging
from google.cloud.logging_v2.services.logging_service_v2 import LoggingServiceV2Client
from google.cloud.logging_v2.services.logging_service_v2.transports import LoggingServiceV2Transport
from google.cloud.logging_v2.handlers.transports import BackgroundThreadTransport
from google.cloud.logging_v2.handlers.transports import SyncTransport
from google.cloud.logging.handlers import CloudLoggingHandler
from google.cloud.logging.handlers import StructuredLogHandler
from google.cloud.logging_v2.handlers import setup_logging
from google.cloud.logging_v2._http import _LoggingAPI
import google.auth.credentials
from google.cloud.logging_v2 import _gapic

_small_text_payload = "hello world"
_large_text_payload = "abcfefghi " * 1000000
_small_json_payload = {'json_key': "hello world"}
_large_json_payload = {f'key_{str(key)}':val for key,val in zip(range(100), ["abcdefghij"*10000 for i in range(100)])}
_payloads = [('small', 'text', _small_text_payload), ('large', 'text', _large_text_payload), ('small', 'json', _small_json_payload), ('large', 'json', _large_json_payload)]



class MockGRPCTransport(LoggingServiceV2Transport):
    """
    Mock for grpc transport.
    Instead of sending logs to server, introduce artificial delay
    """
    def __init__(self, latency=0.1, **kwargs):
        self.latency = latency
        self._wrapped_methods = {self.write_log_entries: self.write_log_entries}

    def write_log_entries(self, *args, **kwargs):
        time.sleep(self.latency)

class MockHttpAPI(_LoggingAPI):
    """
    Mock for http API implementation.
    Instead of sending logs to server, introduce artificial delay
    """
    def __init__(self, client, latency=0.1):
        self._client = client
        self.api_request = lambda **kwargs: time.sleep(latency)

def instrument_function(*args, **kwargs):
    """
    Decorator that takes in a function and returns timing data, 
    along with the functions outpu
    """
    def inner(func):
        profiler = kwargs.pop('profiler')
        profiler.enable()
        start = time.perf_counter()
        func_output = func(*args, **kwargs)
        end = time.perf_counter()
        profiler.disable()
        exec_time = end-start
        return exec_time, func_output
    return inner


def _make_client(mock_network=True, use_grpc=True, mock_latency=0.01):
    """
    Create and return a new test client to manage writing logs
    Can optionally create a real GCP client, or a mock client with artificial network calls
    Can choose between grpc and http client implementations
    """
    if not mock_network:
        # use a real client
        client = google.cloud.logging.Client(_use_grpc=use_grpc)
    elif use_grpc:
        # create a mock grpc client
        mock_transport = MockGRPCTransport(latency=mock_latency)
        gapic_client = LoggingServiceV2Client(transport=mock_transport)
        handwritten_client = mock.Mock()
        api = _gapic._LoggingAPI(gapic_client, handwritten_client)
        creds = mock.Mock(spec=google.auth.credentials.Credentials)
        client = google.cloud.logging.Client(project="my-project",  credentials=creds)
        client._logging_api = api
    else:
        # create a mock http client
        creds = mock.Mock(spec=google.auth.credentials.Credentials)
        client = google.cloud.logging.Client(project="my-project",  credentials=creds)
        mock_http = MockHttpAPI(client, latency=mock_latency)
        client._logging_api = mock_http
    logger = client.logger(name="test_logger")
    end = time.perf_counter()
    return client, logger


def _profile_to_dataframe(pr, keep_n_rows=10):
    result = io.StringIO()
    pstats.Stats(pr,stream=result).sort_stats("cumtime").print_stats()
    result=result.getvalue()
    result='ncalls'+result.split('ncalls')[-1]
    df = pd.DataFrame([x.split(maxsplit=5) for x in result.split('\n')])
    df = df.drop(columns=[1, 2])
    df = df.rename(columns=df.iloc[0]).drop(df.index[0])
    df = df[:keep_n_rows]
    return df

class TestPerformance(unittest.TestCase):

    def setUp(self):
        pd.set_option('display.max_colwidth', None)


    def _print_results(self, profile, results, title):
        console = Console()
        # print header
        print()
        rich.print(Panel(f"[blue]{title} Performance Tests"))
        # print bnchmark results
        rich.print("[cyan]Benchmark")
        benchmark_df = pd.DataFrame(results).sort_values(by='exec_time', ascending=False)
        print(benchmark_df)
        total_time = benchmark_df['exec_time'].sum()
        print(f"Total Benchmark Time: {total_time:.1f}s")
        # print profile information
        print()
        rich.print("[cyan]Breakdown by Function")
        profile_df = _profile_to_dataframe(profile)
        print(profile_df)

    def _get_logger(self, name, handler):
        logger = logging.getLogger(name)
        logger.handlers.clear()
        logger.addHandler(handler)
        logger.propagate = False
        return logger


    def test_client_init_performance(self):
        results = []
        pr = cProfile.Profile()
        for use_grpc, network_str in [(True, 'grpc'), (False, 'http')]:
            # create clients
            exec_time, (client, logger) = instrument_function(mock_network=True, use_grpc=use_grpc, profiler=pr)(_make_client)
            result_dict  = {"protocol":network_str, "exec_time": exec_time}
            results.append(result_dict)
        # print results dataframe
        self._print_results(pr, results, "Client Init")


    def test_structured_logging_performance(self):
        results = []
        pr = cProfile.Profile()

        def profiled_code(logger, payload, num_logs=100):
            for i in range(num_logs):
                logger.error(payload)

        stream = io.StringIO()
        handler = StructuredLogHandler(stream=stream)
        logger = self._get_logger("struct", handler)
        for payload_size, payload_type, payload in _payloads:
            exec_time, _ = instrument_function(logger, payload, profiler=pr)(profiled_code)
            result_dict  = {"payload_type":payload_type, "payload_size":payload_size, "exec_time": exec_time}
            results.append(result_dict)
        # print results dataframe
        self._print_results(pr, results, "StructuredLogHandler")

    def test_cloud_logging_handler_performance(self):
        results = []
        pr = cProfile.Profile()

        def profiled_code(logger, payload, num_logs=100, flush=False):
            for i in range(num_logs):
                logger.error(payload)
            if flush:
                logger.handlers[0].transport.worker.stop()

        for use_grpc, network_str in [(True, 'grpc'), (False, 'http')]:
            # create clients
            client, logger = _make_client(mock_network=True, use_grpc=use_grpc)
            for payload_size, payload_type, payload in _payloads:
                # test cloud logging handler
                for transport_str, transport in [('background', BackgroundThreadTransport), ('sync', SyncTransport)]:
                    handler = CloudLoggingHandler(client, transport=transport)
                    logger = self._get_logger("cloud", handler)
                    exec_time, _ = instrument_function(logger, payload, flush=(transport_str=="background"), profiler=pr)(profiled_code)
                    result_dict  = {"payload_type":payload_type, "payload_size": payload_size, "transport_type":transport_str, "protocol":network_str, "exec_time": exec_time}
                    results.append(result_dict)
        # print results dataframe
        self._print_results(pr, results, "CloudLoggingHandler")

    def test_logging_performance(self):
        results = []
        pr = cProfile.Profile()

        def profiled_code(logger, payload, num_logs=100):
            for i in range(num_logs):
                logger.log(payload)

        for use_grpc, network_str in [(True, 'grpc'), (False, 'http')]:
            # create clients
            client, logger = _make_client(mock_network=True, use_grpc=use_grpc)
            for payload_size, payload_type, payload in _payloads:
                exec_time, _ = instrument_function(logger, payload, profiler=pr)(profiled_code)
                result_dict  = {"payload_type":payload_type, "payload_size":payload_size, "protocol":network_str,  "exec_time": exec_time}
                results.append(result_dict)
        # print results dataframe
        self._print_results(pr, results, "Logger.Log")

    def test_batch_performance(self):
        results = []
        pr = cProfile.Profile()

        def profiled_code(logger, payload, num_logs=100):
            with logger.batch() as batch:
                for i in range(num_logs):
                    batch.log(payload)

        for use_grpc, network_str in [(True, 'grpc'), (False, 'http')]:
            # create clients
            client, logger = _make_client(mock_network=True, use_grpc=use_grpc)
            for payload_size, payload_type, payload in _payloads:
                exec_time, _ = instrument_function(logger, payload, profiler=pr)(profiled_code)
                result_dict  = {"payload_type":payload_type, "payload_size":payload_size, "protocol":network_str,  "exec_time": exec_time}
                results.append(result_dict)
        # print results dataframe
        self._print_results(pr, results, "Batch.Log")


