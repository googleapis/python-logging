# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
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
#

import os
import mock

import grpc
from grpc.experimental import aio
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule

from google import auth
from google.api import distribution_pb2 as distribution  # type: ignore
from google.api import label_pb2 as label  # type: ignore
from google.api import launch_stage_pb2 as launch_stage  # type: ignore
from google.api import metric_pb2 as ga_metric  # type: ignore
from google.api import metric_pb2 as metric  # type: ignore
from google.api_core import client_options
from google.api_core import exceptions
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.auth import credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.logging_v2.services.metrics_service_v2 import (
    MetricsServiceV2AsyncClient,
)
from google.cloud.logging_v2.services.metrics_service_v2 import MetricsServiceV2Client
from google.cloud.logging_v2.services.metrics_service_v2 import pagers
from google.cloud.logging_v2.services.metrics_service_v2 import transports
from google.cloud.logging_v2.types import logging_metrics
from google.oauth2 import service_account
from google.protobuf import duration_pb2 as duration  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return (
        "foo.googleapis.com"
        if ("localhost" in client.DEFAULT_ENDPOINT)
        else client.DEFAULT_ENDPOINT
    )


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert MetricsServiceV2Client._get_default_mtls_endpoint(None) is None
    assert (
        MetricsServiceV2Client._get_default_mtls_endpoint(api_endpoint)
        == api_mtls_endpoint
    )
    assert (
        MetricsServiceV2Client._get_default_mtls_endpoint(api_mtls_endpoint)
        == api_mtls_endpoint
    )
    assert (
        MetricsServiceV2Client._get_default_mtls_endpoint(sandbox_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        MetricsServiceV2Client._get_default_mtls_endpoint(sandbox_mtls_endpoint)
        == sandbox_mtls_endpoint
    )
    assert (
        MetricsServiceV2Client._get_default_mtls_endpoint(non_googleapi)
        == non_googleapi
    )


def test_metrics_service_v2_client_from_service_account_info():
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_info"
    ) as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = MetricsServiceV2Client.from_service_account_info(info)
        assert client.transport._credentials == creds

        assert client.transport._host == "logging.googleapis.com:443"


@pytest.mark.parametrize(
    "client_class", [MetricsServiceV2Client, MetricsServiceV2AsyncClient,]
)
def test_metrics_service_v2_client_from_service_account_file(client_class):
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(
        service_account.Credentials, "from_service_account_file"
    ) as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json")
        assert client.transport._credentials == creds

        client = client_class.from_service_account_json("dummy/file/path.json")
        assert client.transport._credentials == creds

        assert client.transport._host == "logging.googleapis.com:443"


def test_metrics_service_v2_client_get_transport_class():
    transport = MetricsServiceV2Client.get_transport_class()
    available_transports = [
        transports.MetricsServiceV2GrpcTransport,
    ]
    assert transport in available_transports

    transport = MetricsServiceV2Client.get_transport_class("grpc")
    assert transport == transports.MetricsServiceV2GrpcTransport


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (MetricsServiceV2Client, transports.MetricsServiceV2GrpcTransport, "grpc"),
        (
            MetricsServiceV2AsyncClient,
            transports.MetricsServiceV2GrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
@mock.patch.object(
    MetricsServiceV2Client,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(MetricsServiceV2Client),
)
@mock.patch.object(
    MetricsServiceV2AsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(MetricsServiceV2AsyncClient),
)
def test_metrics_service_v2_client_client_options(
    client_class, transport_class, transport_name
):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(MetricsServiceV2Client, "get_transport_class") as gtc:
        transport = transport_class(credentials=credentials.AnonymousCredentials())
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(MetricsServiceV2Client, "get_transport_class") as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                ssl_channel_credentials=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class()
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                ssl_channel_credentials=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class()

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}
    ):
        with pytest.raises(ValueError):
            client = client_class()

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name,use_client_cert_env",
    [
        (
            MetricsServiceV2Client,
            transports.MetricsServiceV2GrpcTransport,
            "grpc",
            "true",
        ),
        (
            MetricsServiceV2AsyncClient,
            transports.MetricsServiceV2GrpcAsyncIOTransport,
            "grpc_asyncio",
            "true",
        ),
        (
            MetricsServiceV2Client,
            transports.MetricsServiceV2GrpcTransport,
            "grpc",
            "false",
        ),
        (
            MetricsServiceV2AsyncClient,
            transports.MetricsServiceV2GrpcAsyncIOTransport,
            "grpc_asyncio",
            "false",
        ),
    ],
)
@mock.patch.object(
    MetricsServiceV2Client,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(MetricsServiceV2Client),
)
@mock.patch.object(
    MetricsServiceV2AsyncClient,
    "DEFAULT_ENDPOINT",
    modify_default_endpoint(MetricsServiceV2AsyncClient),
)
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_metrics_service_v2_client_mtls_env_auto(
    client_class, transport_class, transport_name, use_client_cert_env
):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        options = client_options.ClientOptions(
            client_cert_source=client_cert_source_callback
        )
        with mock.patch.object(transport_class, "__init__") as patched:
            ssl_channel_creds = mock.Mock()
            with mock.patch(
                "grpc.ssl_channel_credentials", return_value=ssl_channel_creds
            ):
                patched.return_value = None
                client = client_class(client_options=options)

                if use_client_cert_env == "false":
                    expected_ssl_channel_creds = None
                    expected_host = client.DEFAULT_ENDPOINT
                else:
                    expected_ssl_channel_creds = ssl_channel_creds
                    expected_host = client.DEFAULT_MTLS_ENDPOINT

                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=expected_host,
                    scopes=None,
                    ssl_channel_credentials=expected_ssl_channel_creds,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.grpc.SslCredentials.__init__", return_value=None
            ):
                with mock.patch(
                    "google.auth.transport.grpc.SslCredentials.is_mtls",
                    new_callable=mock.PropertyMock,
                ) as is_mtls_mock:
                    with mock.patch(
                        "google.auth.transport.grpc.SslCredentials.ssl_credentials",
                        new_callable=mock.PropertyMock,
                    ) as ssl_credentials_mock:
                        if use_client_cert_env == "false":
                            is_mtls_mock.return_value = False
                            ssl_credentials_mock.return_value = None
                            expected_host = client.DEFAULT_ENDPOINT
                            expected_ssl_channel_creds = None
                        else:
                            is_mtls_mock.return_value = True
                            ssl_credentials_mock.return_value = mock.Mock()
                            expected_host = client.DEFAULT_MTLS_ENDPOINT
                            expected_ssl_channel_creds = (
                                ssl_credentials_mock.return_value
                            )

                        patched.return_value = None
                        client = client_class()
                        patched.assert_called_once_with(
                            credentials=None,
                            credentials_file=None,
                            host=expected_host,
                            scopes=None,
                            ssl_channel_credentials=expected_ssl_channel_creds,
                            quota_project_id=None,
                            client_info=transports.base.DEFAULT_CLIENT_INFO,
                        )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(
        os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}
    ):
        with mock.patch.object(transport_class, "__init__") as patched:
            with mock.patch(
                "google.auth.transport.grpc.SslCredentials.__init__", return_value=None
            ):
                with mock.patch(
                    "google.auth.transport.grpc.SslCredentials.is_mtls",
                    new_callable=mock.PropertyMock,
                ) as is_mtls_mock:
                    is_mtls_mock.return_value = False
                    patched.return_value = None
                    client = client_class()
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=client.DEFAULT_ENDPOINT,
                        scopes=None,
                        ssl_channel_credentials=None,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                    )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (MetricsServiceV2Client, transports.MetricsServiceV2GrpcTransport, "grpc"),
        (
            MetricsServiceV2AsyncClient,
            transports.MetricsServiceV2GrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_metrics_service_v2_client_client_options_scopes(
    client_class, transport_class, transport_name
):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(scopes=["1", "2"],)
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


@pytest.mark.parametrize(
    "client_class,transport_class,transport_name",
    [
        (MetricsServiceV2Client, transports.MetricsServiceV2GrpcTransport, "grpc"),
        (
            MetricsServiceV2AsyncClient,
            transports.MetricsServiceV2GrpcAsyncIOTransport,
            "grpc_asyncio",
        ),
    ],
)
def test_metrics_service_v2_client_client_options_credentials_file(
    client_class, transport_class, transport_name
):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(credentials_file="credentials.json")
    with mock.patch.object(transport_class, "__init__") as patched:
        patched.return_value = None
        client = client_class(client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_metrics_service_v2_client_client_options_from_dict():
    with mock.patch(
        "google.cloud.logging_v2.services.metrics_service_v2.transports.MetricsServiceV2GrpcTransport.__init__"
    ) as grpc_transport:
        grpc_transport.return_value = None
        client = MetricsServiceV2Client(
            client_options={"api_endpoint": "squid.clam.whelk"}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            ssl_channel_credentials=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
        )


def test_list_log_metrics(
    transport: str = "grpc", request_type=logging_metrics.ListLogMetricsRequest
):
    client = MetricsServiceV2Client(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_log_metrics), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_metrics.ListLogMetricsResponse(
            next_page_token="next_page_token_value",
        )

        response = client.list_log_metrics(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == logging_metrics.ListLogMetricsRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, pagers.ListLogMetricsPager)

    assert response.next_page_token == "next_page_token_value"


def test_list_log_metrics_from_dict():
    test_list_log_metrics(request_type=dict)


@pytest.mark.asyncio
async def test_list_log_metrics_async(
    transport: str = "grpc_asyncio", request_type=logging_metrics.ListLogMetricsRequest
):
    client = MetricsServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_log_metrics), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            logging_metrics.ListLogMetricsResponse(
                next_page_token="next_page_token_value",
            )
        )

        response = await client.list_log_metrics(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == logging_metrics.ListLogMetricsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListLogMetricsAsyncPager)

    assert response.next_page_token == "next_page_token_value"


@pytest.mark.asyncio
async def test_list_log_metrics_async_from_dict():
    await test_list_log_metrics_async(request_type=dict)


def test_list_log_metrics_field_headers():
    client = MetricsServiceV2Client(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_metrics.ListLogMetricsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_log_metrics), "__call__") as call:
        call.return_value = logging_metrics.ListLogMetricsResponse()

        client.list_log_metrics(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_list_log_metrics_field_headers_async():
    client = MetricsServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_metrics.ListLogMetricsRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_log_metrics), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            logging_metrics.ListLogMetricsResponse()
        )

        await client.list_log_metrics(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_list_log_metrics_flattened():
    client = MetricsServiceV2Client(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_log_metrics), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_metrics.ListLogMetricsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_log_metrics(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


def test_list_log_metrics_flattened_error():
    client = MetricsServiceV2Client(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_log_metrics(
            logging_metrics.ListLogMetricsRequest(), parent="parent_value",
        )


@pytest.mark.asyncio
async def test_list_log_metrics_flattened_async():
    client = MetricsServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_log_metrics), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_metrics.ListLogMetricsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            logging_metrics.ListLogMetricsResponse()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_log_metrics(parent="parent_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"


@pytest.mark.asyncio
async def test_list_log_metrics_flattened_error_async():
    client = MetricsServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_log_metrics(
            logging_metrics.ListLogMetricsRequest(), parent="parent_value",
        )


def test_list_log_metrics_pager():
    client = MetricsServiceV2Client(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_log_metrics), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging_metrics.ListLogMetricsResponse(
                metrics=[
                    logging_metrics.LogMetric(),
                    logging_metrics.LogMetric(),
                    logging_metrics.LogMetric(),
                ],
                next_page_token="abc",
            ),
            logging_metrics.ListLogMetricsResponse(metrics=[], next_page_token="def",),
            logging_metrics.ListLogMetricsResponse(
                metrics=[logging_metrics.LogMetric(),], next_page_token="ghi",
            ),
            logging_metrics.ListLogMetricsResponse(
                metrics=[logging_metrics.LogMetric(), logging_metrics.LogMetric(),],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", ""),)),
        )
        pager = client.list_log_metrics(request={})

        assert pager._metadata == metadata

        results = [i for i in pager]
        assert len(results) == 6
        assert all(isinstance(i, logging_metrics.LogMetric) for i in results)


def test_list_log_metrics_pages():
    client = MetricsServiceV2Client(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.list_log_metrics), "__call__") as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging_metrics.ListLogMetricsResponse(
                metrics=[
                    logging_metrics.LogMetric(),
                    logging_metrics.LogMetric(),
                    logging_metrics.LogMetric(),
                ],
                next_page_token="abc",
            ),
            logging_metrics.ListLogMetricsResponse(metrics=[], next_page_token="def",),
            logging_metrics.ListLogMetricsResponse(
                metrics=[logging_metrics.LogMetric(),], next_page_token="ghi",
            ),
            logging_metrics.ListLogMetricsResponse(
                metrics=[logging_metrics.LogMetric(), logging_metrics.LogMetric(),],
            ),
            RuntimeError,
        )
        pages = list(client.list_log_metrics(request={}).pages)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


@pytest.mark.asyncio
async def test_list_log_metrics_async_pager():
    client = MetricsServiceV2AsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_log_metrics), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging_metrics.ListLogMetricsResponse(
                metrics=[
                    logging_metrics.LogMetric(),
                    logging_metrics.LogMetric(),
                    logging_metrics.LogMetric(),
                ],
                next_page_token="abc",
            ),
            logging_metrics.ListLogMetricsResponse(metrics=[], next_page_token="def",),
            logging_metrics.ListLogMetricsResponse(
                metrics=[logging_metrics.LogMetric(),], next_page_token="ghi",
            ),
            logging_metrics.ListLogMetricsResponse(
                metrics=[logging_metrics.LogMetric(), logging_metrics.LogMetric(),],
            ),
            RuntimeError,
        )
        async_pager = await client.list_log_metrics(request={},)
        assert async_pager.next_page_token == "abc"
        responses = []
        async for response in async_pager:
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, logging_metrics.LogMetric) for i in responses)


@pytest.mark.asyncio
async def test_list_log_metrics_async_pages():
    client = MetricsServiceV2AsyncClient(credentials=credentials.AnonymousCredentials,)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.list_log_metrics), "__call__", new_callable=mock.AsyncMock
    ) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            logging_metrics.ListLogMetricsResponse(
                metrics=[
                    logging_metrics.LogMetric(),
                    logging_metrics.LogMetric(),
                    logging_metrics.LogMetric(),
                ],
                next_page_token="abc",
            ),
            logging_metrics.ListLogMetricsResponse(metrics=[], next_page_token="def",),
            logging_metrics.ListLogMetricsResponse(
                metrics=[logging_metrics.LogMetric(),], next_page_token="ghi",
            ),
            logging_metrics.ListLogMetricsResponse(
                metrics=[logging_metrics.LogMetric(), logging_metrics.LogMetric(),],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_log_metrics(request={})).pages:
            pages.append(page_)
        for page_, token in zip(pages, ["abc", "def", "ghi", ""]):
            assert page_.raw_page.next_page_token == token


def test_get_log_metric(
    transport: str = "grpc", request_type=logging_metrics.GetLogMetricRequest
):
    client = MetricsServiceV2Client(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_log_metric), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_metrics.LogMetric(
            name="name_value",
            description="description_value",
            filter="filter_value",
            value_extractor="value_extractor_value",
            version=logging_metrics.LogMetric.ApiVersion.V1,
        )

        response = client.get_log_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == logging_metrics.GetLogMetricRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, logging_metrics.LogMetric)

    assert response.name == "name_value"

    assert response.description == "description_value"

    assert response.filter == "filter_value"

    assert response.value_extractor == "value_extractor_value"

    assert response.version == logging_metrics.LogMetric.ApiVersion.V1


def test_get_log_metric_from_dict():
    test_get_log_metric(request_type=dict)


@pytest.mark.asyncio
async def test_get_log_metric_async(
    transport: str = "grpc_asyncio", request_type=logging_metrics.GetLogMetricRequest
):
    client = MetricsServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_log_metric), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            logging_metrics.LogMetric(
                name="name_value",
                description="description_value",
                filter="filter_value",
                value_extractor="value_extractor_value",
                version=logging_metrics.LogMetric.ApiVersion.V1,
            )
        )

        response = await client.get_log_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == logging_metrics.GetLogMetricRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging_metrics.LogMetric)

    assert response.name == "name_value"

    assert response.description == "description_value"

    assert response.filter == "filter_value"

    assert response.value_extractor == "value_extractor_value"

    assert response.version == logging_metrics.LogMetric.ApiVersion.V1


@pytest.mark.asyncio
async def test_get_log_metric_async_from_dict():
    await test_get_log_metric_async(request_type=dict)


def test_get_log_metric_field_headers():
    client = MetricsServiceV2Client(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_metrics.GetLogMetricRequest()
    request.metric_name = "metric_name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_log_metric), "__call__") as call:
        call.return_value = logging_metrics.LogMetric()

        client.get_log_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "metric_name=metric_name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_get_log_metric_field_headers_async():
    client = MetricsServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_metrics.GetLogMetricRequest()
    request.metric_name = "metric_name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_log_metric), "__call__") as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            logging_metrics.LogMetric()
        )

        await client.get_log_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "metric_name=metric_name/value",) in kw["metadata"]


def test_get_log_metric_flattened():
    client = MetricsServiceV2Client(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_log_metric), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_metrics.LogMetric()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_log_metric(metric_name="metric_name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].metric_name == "metric_name_value"


def test_get_log_metric_flattened_error():
    client = MetricsServiceV2Client(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_log_metric(
            logging_metrics.GetLogMetricRequest(), metric_name="metric_name_value",
        )


@pytest.mark.asyncio
async def test_get_log_metric_flattened_async():
    client = MetricsServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(type(client.transport.get_log_metric), "__call__") as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_metrics.LogMetric()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            logging_metrics.LogMetric()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_log_metric(metric_name="metric_name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].metric_name == "metric_name_value"


@pytest.mark.asyncio
async def test_get_log_metric_flattened_error_async():
    client = MetricsServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_log_metric(
            logging_metrics.GetLogMetricRequest(), metric_name="metric_name_value",
        )


def test_create_log_metric(
    transport: str = "grpc", request_type=logging_metrics.CreateLogMetricRequest
):
    client = MetricsServiceV2Client(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_log_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_metrics.LogMetric(
            name="name_value",
            description="description_value",
            filter="filter_value",
            value_extractor="value_extractor_value",
            version=logging_metrics.LogMetric.ApiVersion.V1,
        )

        response = client.create_log_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == logging_metrics.CreateLogMetricRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, logging_metrics.LogMetric)

    assert response.name == "name_value"

    assert response.description == "description_value"

    assert response.filter == "filter_value"

    assert response.value_extractor == "value_extractor_value"

    assert response.version == logging_metrics.LogMetric.ApiVersion.V1


def test_create_log_metric_from_dict():
    test_create_log_metric(request_type=dict)


@pytest.mark.asyncio
async def test_create_log_metric_async(
    transport: str = "grpc_asyncio", request_type=logging_metrics.CreateLogMetricRequest
):
    client = MetricsServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_log_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            logging_metrics.LogMetric(
                name="name_value",
                description="description_value",
                filter="filter_value",
                value_extractor="value_extractor_value",
                version=logging_metrics.LogMetric.ApiVersion.V1,
            )
        )

        response = await client.create_log_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == logging_metrics.CreateLogMetricRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging_metrics.LogMetric)

    assert response.name == "name_value"

    assert response.description == "description_value"

    assert response.filter == "filter_value"

    assert response.value_extractor == "value_extractor_value"

    assert response.version == logging_metrics.LogMetric.ApiVersion.V1


@pytest.mark.asyncio
async def test_create_log_metric_async_from_dict():
    await test_create_log_metric_async(request_type=dict)


def test_create_log_metric_field_headers():
    client = MetricsServiceV2Client(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_metrics.CreateLogMetricRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_log_metric), "__call__"
    ) as call:
        call.return_value = logging_metrics.LogMetric()

        client.create_log_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_create_log_metric_field_headers_async():
    client = MetricsServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_metrics.CreateLogMetricRequest()
    request.parent = "parent/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_log_metric), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            logging_metrics.LogMetric()
        )

        await client.create_log_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "parent=parent/value",) in kw["metadata"]


def test_create_log_metric_flattened():
    client = MetricsServiceV2Client(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_log_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_metrics.LogMetric()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_log_metric(
            parent="parent_value", metric=logging_metrics.LogMetric(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].metric == logging_metrics.LogMetric(name="name_value")


def test_create_log_metric_flattened_error():
    client = MetricsServiceV2Client(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_log_metric(
            logging_metrics.CreateLogMetricRequest(),
            parent="parent_value",
            metric=logging_metrics.LogMetric(name="name_value"),
        )


@pytest.mark.asyncio
async def test_create_log_metric_flattened_async():
    client = MetricsServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.create_log_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_metrics.LogMetric()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            logging_metrics.LogMetric()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_log_metric(
            parent="parent_value", metric=logging_metrics.LogMetric(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].parent == "parent_value"

        assert args[0].metric == logging_metrics.LogMetric(name="name_value")


@pytest.mark.asyncio
async def test_create_log_metric_flattened_error_async():
    client = MetricsServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_log_metric(
            logging_metrics.CreateLogMetricRequest(),
            parent="parent_value",
            metric=logging_metrics.LogMetric(name="name_value"),
        )


def test_update_log_metric(
    transport: str = "grpc", request_type=logging_metrics.UpdateLogMetricRequest
):
    client = MetricsServiceV2Client(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_log_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_metrics.LogMetric(
            name="name_value",
            description="description_value",
            filter="filter_value",
            value_extractor="value_extractor_value",
            version=logging_metrics.LogMetric.ApiVersion.V1,
        )

        response = client.update_log_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == logging_metrics.UpdateLogMetricRequest()

    # Establish that the response is the type that we expect.

    assert isinstance(response, logging_metrics.LogMetric)

    assert response.name == "name_value"

    assert response.description == "description_value"

    assert response.filter == "filter_value"

    assert response.value_extractor == "value_extractor_value"

    assert response.version == logging_metrics.LogMetric.ApiVersion.V1


def test_update_log_metric_from_dict():
    test_update_log_metric(request_type=dict)


@pytest.mark.asyncio
async def test_update_log_metric_async(
    transport: str = "grpc_asyncio", request_type=logging_metrics.UpdateLogMetricRequest
):
    client = MetricsServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_log_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            logging_metrics.LogMetric(
                name="name_value",
                description="description_value",
                filter="filter_value",
                value_extractor="value_extractor_value",
                version=logging_metrics.LogMetric.ApiVersion.V1,
            )
        )

        response = await client.update_log_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == logging_metrics.UpdateLogMetricRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, logging_metrics.LogMetric)

    assert response.name == "name_value"

    assert response.description == "description_value"

    assert response.filter == "filter_value"

    assert response.value_extractor == "value_extractor_value"

    assert response.version == logging_metrics.LogMetric.ApiVersion.V1


@pytest.mark.asyncio
async def test_update_log_metric_async_from_dict():
    await test_update_log_metric_async(request_type=dict)


def test_update_log_metric_field_headers():
    client = MetricsServiceV2Client(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_metrics.UpdateLogMetricRequest()
    request.metric_name = "metric_name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_log_metric), "__call__"
    ) as call:
        call.return_value = logging_metrics.LogMetric()

        client.update_log_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "metric_name=metric_name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_update_log_metric_field_headers_async():
    client = MetricsServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_metrics.UpdateLogMetricRequest()
    request.metric_name = "metric_name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_log_metric), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            logging_metrics.LogMetric()
        )

        await client.update_log_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "metric_name=metric_name/value",) in kw["metadata"]


def test_update_log_metric_flattened():
    client = MetricsServiceV2Client(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_log_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_metrics.LogMetric()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_log_metric(
            metric_name="metric_name_value",
            metric=logging_metrics.LogMetric(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].metric_name == "metric_name_value"

        assert args[0].metric == logging_metrics.LogMetric(name="name_value")


def test_update_log_metric_flattened_error():
    client = MetricsServiceV2Client(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_log_metric(
            logging_metrics.UpdateLogMetricRequest(),
            metric_name="metric_name_value",
            metric=logging_metrics.LogMetric(name="name_value"),
        )


@pytest.mark.asyncio
async def test_update_log_metric_flattened_async():
    client = MetricsServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.update_log_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = logging_metrics.LogMetric()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            logging_metrics.LogMetric()
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_log_metric(
            metric_name="metric_name_value",
            metric=logging_metrics.LogMetric(name="name_value"),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].metric_name == "metric_name_value"

        assert args[0].metric == logging_metrics.LogMetric(name="name_value")


@pytest.mark.asyncio
async def test_update_log_metric_flattened_error_async():
    client = MetricsServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_log_metric(
            logging_metrics.UpdateLogMetricRequest(),
            metric_name="metric_name_value",
            metric=logging_metrics.LogMetric(name="name_value"),
        )


def test_delete_log_metric(
    transport: str = "grpc", request_type=logging_metrics.DeleteLogMetricRequest
):
    client = MetricsServiceV2Client(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_log_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        response = client.delete_log_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == logging_metrics.DeleteLogMetricRequest()

    # Establish that the response is the type that we expect.
    assert response is None


def test_delete_log_metric_from_dict():
    test_delete_log_metric(request_type=dict)


@pytest.mark.asyncio
async def test_delete_log_metric_async(
    transport: str = "grpc_asyncio", request_type=logging_metrics.DeleteLogMetricRequest
):
    client = MetricsServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(), transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_log_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        response = await client.delete_log_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0] == logging_metrics.DeleteLogMetricRequest()

    # Establish that the response is the type that we expect.
    assert response is None


@pytest.mark.asyncio
async def test_delete_log_metric_async_from_dict():
    await test_delete_log_metric_async(request_type=dict)


def test_delete_log_metric_field_headers():
    client = MetricsServiceV2Client(credentials=credentials.AnonymousCredentials(),)

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_metrics.DeleteLogMetricRequest()
    request.metric_name = "metric_name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_log_metric), "__call__"
    ) as call:
        call.return_value = None

        client.delete_log_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "metric_name=metric_name/value",) in kw["metadata"]


@pytest.mark.asyncio
async def test_delete_log_metric_field_headers_async():
    client = MetricsServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = logging_metrics.DeleteLogMetricRequest()
    request.metric_name = "metric_name/value"

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_log_metric), "__call__"
    ) as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)

        await client.delete_log_metric(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert ("x-goog-request-params", "metric_name=metric_name/value",) in kw["metadata"]


def test_delete_log_metric_flattened():
    client = MetricsServiceV2Client(credentials=credentials.AnonymousCredentials(),)

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_log_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_log_metric(metric_name="metric_name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0].metric_name == "metric_name_value"


def test_delete_log_metric_flattened_error():
    client = MetricsServiceV2Client(credentials=credentials.AnonymousCredentials(),)

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_log_metric(
            logging_metrics.DeleteLogMetricRequest(), metric_name="metric_name_value",
        )


@pytest.mark.asyncio
async def test_delete_log_metric_flattened_async():
    client = MetricsServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
        type(client.transport.delete_log_metric), "__call__"
    ) as call:
        # Designate an appropriate return value for the call.
        call.return_value = None

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(None)
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_log_metric(metric_name="metric_name_value",)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]

        assert args[0].metric_name == "metric_name_value"


@pytest.mark.asyncio
async def test_delete_log_metric_flattened_error_async():
    client = MetricsServiceV2AsyncClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_log_metric(
            logging_metrics.DeleteLogMetricRequest(), metric_name="metric_name_value",
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.MetricsServiceV2GrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = MetricsServiceV2Client(
            credentials=credentials.AnonymousCredentials(), transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.MetricsServiceV2GrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = MetricsServiceV2Client(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.MetricsServiceV2GrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = MetricsServiceV2Client(
            client_options={"scopes": ["1", "2"]}, transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.MetricsServiceV2GrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = MetricsServiceV2Client(transport=transport)
    assert client.transport is transport


def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.MetricsServiceV2GrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.MetricsServiceV2GrpcAsyncIOTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.MetricsServiceV2GrpcTransport,
        transports.MetricsServiceV2GrpcAsyncIOTransport,
    ],
)
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = MetricsServiceV2Client(credentials=credentials.AnonymousCredentials(),)
    assert isinstance(client.transport, transports.MetricsServiceV2GrpcTransport,)


def test_metrics_service_v2_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(exceptions.DuplicateCredentialArgs):
        transport = transports.MetricsServiceV2Transport(
            credentials=credentials.AnonymousCredentials(),
            credentials_file="credentials.json",
        )


def test_metrics_service_v2_base_transport():
    # Instantiate the base transport.
    with mock.patch(
        "google.cloud.logging_v2.services.metrics_service_v2.transports.MetricsServiceV2Transport.__init__"
    ) as Transport:
        Transport.return_value = None
        transport = transports.MetricsServiceV2Transport(
            credentials=credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        "list_log_metrics",
        "get_log_metric",
        "create_log_metric",
        "update_log_metric",
        "delete_log_metric",
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_metrics_service_v2_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(
        auth, "load_credentials_from_file"
    ) as load_creds, mock.patch(
        "google.cloud.logging_v2.services.metrics_service_v2.transports.MetricsServiceV2Transport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        load_creds.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.MetricsServiceV2Transport(
            credentials_file="credentials.json", quota_project_id="octopus",
        )
        load_creds.assert_called_once_with(
            "credentials.json",
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
                "https://www.googleapis.com/auth/logging.admin",
                "https://www.googleapis.com/auth/logging.read",
                "https://www.googleapis.com/auth/logging.write",
            ),
            quota_project_id="octopus",
        )


def test_metrics_service_v2_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(auth, "default") as adc, mock.patch(
        "google.cloud.logging_v2.services.metrics_service_v2.transports.MetricsServiceV2Transport._prep_wrapped_messages"
    ) as Transport:
        Transport.return_value = None
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transport = transports.MetricsServiceV2Transport()
        adc.assert_called_once()


def test_metrics_service_v2_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        MetricsServiceV2Client()
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
                "https://www.googleapis.com/auth/logging.admin",
                "https://www.googleapis.com/auth/logging.read",
                "https://www.googleapis.com/auth/logging.write",
            ),
            quota_project_id=None,
        )


def test_metrics_service_v2_transport_auth_adc():
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(auth, "default") as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        transports.MetricsServiceV2GrpcTransport(
            host="squid.clam.whelk", quota_project_id="octopus"
        )
        adc.assert_called_once_with(
            scopes=(
                "https://www.googleapis.com/auth/cloud-platform",
                "https://www.googleapis.com/auth/cloud-platform.read-only",
                "https://www.googleapis.com/auth/logging.admin",
                "https://www.googleapis.com/auth/logging.read",
                "https://www.googleapis.com/auth/logging.write",
            ),
            quota_project_id="octopus",
        )


def test_metrics_service_v2_host_no_port():
    client = MetricsServiceV2Client(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="logging.googleapis.com"
        ),
    )
    assert client.transport._host == "logging.googleapis.com:443"


def test_metrics_service_v2_host_with_port():
    client = MetricsServiceV2Client(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(
            api_endpoint="logging.googleapis.com:8000"
        ),
    )
    assert client.transport._host == "logging.googleapis.com:8000"


def test_metrics_service_v2_grpc_transport_channel():
    channel = grpc.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.MetricsServiceV2GrpcTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_metrics_service_v2_grpc_asyncio_transport_channel():
    channel = aio.secure_channel("http://localhost/", grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.MetricsServiceV2GrpcAsyncIOTransport(
        host="squid.clam.whelk", channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.MetricsServiceV2GrpcTransport,
        transports.MetricsServiceV2GrpcAsyncIOTransport,
    ],
)
def test_metrics_service_v2_transport_channel_mtls_with_client_cert_source(
    transport_class,
):
    with mock.patch(
        "grpc.ssl_channel_credentials", autospec=True
    ) as grpc_ssl_channel_cred:
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(auth, "default") as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=(
                    "https://www.googleapis.com/auth/cloud-platform",
                    "https://www.googleapis.com/auth/cloud-platform.read-only",
                    "https://www.googleapis.com/auth/logging.admin",
                    "https://www.googleapis.com/auth/logging.read",
                    "https://www.googleapis.com/auth/logging.write",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.MetricsServiceV2GrpcTransport,
        transports.MetricsServiceV2GrpcAsyncIOTransport,
    ],
)
def test_metrics_service_v2_transport_channel_mtls_with_adc(transport_class):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(
            transport_class, "create_channel"
        ) as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=(
                    "https://www.googleapis.com/auth/cloud-platform",
                    "https://www.googleapis.com/auth/cloud-platform.read-only",
                    "https://www.googleapis.com/auth/logging.admin",
                    "https://www.googleapis.com/auth/logging.read",
                    "https://www.googleapis.com/auth/logging.write",
                ),
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_log_metric_path():
    project = "squid"
    metric = "clam"

    expected = "projects/{project}/metrics/{metric}".format(
        project=project, metric=metric,
    )
    actual = MetricsServiceV2Client.log_metric_path(project, metric)
    assert expected == actual


def test_parse_log_metric_path():
    expected = {
        "project": "whelk",
        "metric": "octopus",
    }
    path = MetricsServiceV2Client.log_metric_path(**expected)

    # Check that the path construction is reversible.
    actual = MetricsServiceV2Client.parse_log_metric_path(path)
    assert expected == actual


def test_common_billing_account_path():
    billing_account = "oyster"

    expected = "billingAccounts/{billing_account}".format(
        billing_account=billing_account,
    )
    actual = MetricsServiceV2Client.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "nudibranch",
    }
    path = MetricsServiceV2Client.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = MetricsServiceV2Client.parse_common_billing_account_path(path)
    assert expected == actual


def test_common_folder_path():
    folder = "cuttlefish"

    expected = "folders/{folder}".format(folder=folder,)
    actual = MetricsServiceV2Client.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "mussel",
    }
    path = MetricsServiceV2Client.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = MetricsServiceV2Client.parse_common_folder_path(path)
    assert expected == actual


def test_common_organization_path():
    organization = "winkle"

    expected = "organizations/{organization}".format(organization=organization,)
    actual = MetricsServiceV2Client.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "nautilus",
    }
    path = MetricsServiceV2Client.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = MetricsServiceV2Client.parse_common_organization_path(path)
    assert expected == actual


def test_common_project_path():
    project = "scallop"

    expected = "projects/{project}".format(project=project,)
    actual = MetricsServiceV2Client.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "abalone",
    }
    path = MetricsServiceV2Client.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = MetricsServiceV2Client.parse_common_project_path(path)
    assert expected == actual


def test_common_location_path():
    project = "squid"
    location = "clam"

    expected = "projects/{project}/locations/{location}".format(
        project=project, location=location,
    )
    actual = MetricsServiceV2Client.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "whelk",
        "location": "octopus",
    }
    path = MetricsServiceV2Client.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = MetricsServiceV2Client.parse_common_location_path(path)
    assert expected == actual


def test_client_withDEFAULT_CLIENT_INFO():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(
        transports.MetricsServiceV2Transport, "_prep_wrapped_messages"
    ) as prep:
        client = MetricsServiceV2Client(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(
        transports.MetricsServiceV2Transport, "_prep_wrapped_messages"
    ) as prep:
        transport_class = MetricsServiceV2Client.get_transport_class()
        transport = transport_class(
            credentials=credentials.AnonymousCredentials(), client_info=client_info,
        )
        prep.assert_called_once_with(client_info)
