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


def instrument_function(description, profiler, fn, *fn_args, **fn_kwargs):
    """
    Takes in a function and related data, runs it, and returns a dictionary
    filled with instrumentation data
    """
    profiler.enable()
    start = time.perf_counter()
    fn_out = fn(*fn_args, **fn_kwargs)
    end = time.perf_counter()
    profiler.disable()
    exec_time = end-start
    result_dict  = {"description": description, "exec_time": exec_time}
    return result_dict, fn_out


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

def logger_log(logger, payload, num_logs=100):
    # create logs
    for i in range(num_logs):
        logger.log(payload)

def batch_log(logger, payload, num_logs=100):
    # create logs
    with logger.batch() as batch:
        for i in range(num_logs):
            batch.log(payload)

def structured_log_handler(payload, num_logs=100):
    stream = io.StringIO()
    handler = StructuredLogHandler(stream=stream)
    logger = logging.getLogger("struct")
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.propagate = False
    for i in range(num_logs):
        logger.error(payload)


def cloud_log_handler(client, transport, payload, num_logs=100):
    handler = CloudLoggingHandler(client, transport=transport)
    logger = logging.getLogger("cloud")
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.propagate = False
    for i in range(num_logs):
        logger.error(payload)

def _create_payload(payload_size=1000000, json=False):
    log_payload = "message "
    log_payload = log_payload * math.ceil(payload_size / len(log_payload))
    log_payload = log_payload[:payload_size]
    if json:
        log_payload = {"key": log_payload}
    return log_payload


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

def _save_results(benchmark_df, profile_df, save_dir="./performance_test_output"):
    Path(save_dir).mkdir(parents=True, exist_ok=True)
    benchmark_df.to_csv(f"{save_dir}/latest_benchmark.csv", index=False)
    profile_df.to_csv(f"{save_dir}/latest_profile.csv", index=False)

def _load_prev_results(load_dir='./performance_test_output'):
    benchmark_df = pd.read_csv(f"{load_dir}/latest_benchmark.csv")
    profile_df = pd.read_csv(f"{load_dir}/latest_profile.csv")
    return benchmark_df, profile_df

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

    def test_client_init_performance(self):
        results = []
        pr = cProfile.Profile()
        for use_grpc, network_str in [(True, 'grpc'), (False, 'http')]:
            # create clients
            description = f"{network_str} client setup"
            result, (client, logger) = instrument_function(description, pr, _make_client, mock_network=True, use_grpc=use_grpc)
            results.append(result)
        # print results dataframe
        self._print_results(pr, results, "Client Init")


    def test_structured_logging_performance(self):
        results = []
        pr = cProfile.Profile()
        for payload_str, is_json_payload in [('json', True), ('text', False)]:
            description = f"StructuredLogHandler with {payload_str} payload"
            log_payload = _create_payload(json=is_json_payload)
            result, _ = instrument_function(description, pr, structured_log_handler, log_payload)
            results.append(result)
        # print results dataframe
        self._print_results(pr, results, "StructuredLogHandler")

    def test_cloud_logging_handler_performance(self):
        results = []
        pr = cProfile.Profile()

        for use_grpc, network_str in [(True, 'grpc'), (False, 'http')]:
            # create clients
            client, logger = _make_client(mock_network=True, use_grpc=use_grpc)
            for payload_str, is_json_payload in [('json', True), ('text', False)]:
                log_payload = _create_payload(is_json_payload)
                # test cloud logging handler
                for transport_str, transport in [('background', BackgroundThreadTransport), ('sync', SyncTransport)]:
                    description = f"CloudLoggingHandler over {network_str} with {transport_str} transport and {payload_str} payload"
                    result, _ = instrument_function(description, pr, cloud_log_handler, client, transport, log_payload)
                    results.append(result)
        # print results dataframe
        self._print_results(pr, results, "CloudLoggingHandler")

    def test_logging_performance(self):
        results = []
        pr = cProfile.Profile()

        for use_grpc, network_str in [(True, 'grpc'), (False, 'http')]:
            # create clients
            client, logger = _make_client(mock_network=True, use_grpc=use_grpc)
            for payload_str, is_json_payload in [('json', True), ('text', False)]:
                log_payload = _create_payload(is_json_payload)
                # test logger.log and batch.log APIs
                for fn_str, fn_val in [('logger.log', logger_log), ('batch.log', batch_log)]:
                    description = f"{fn_str} over {network_str} with {payload_str} payload"
                    result, _ = instrument_function(description, pr, fn_val, logger, log_payload)
                    results.append(result)
        # print results dataframe
        self._print_results(pr, results, "Logger.Log")

