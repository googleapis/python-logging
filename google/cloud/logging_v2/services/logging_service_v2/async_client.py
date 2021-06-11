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
from collections import OrderedDict
import functools
import re
from typing import (
    Dict,
    AsyncIterable,
    Awaitable,
    AsyncIterator,
    Sequence,
    Tuple,
    Type,
    Union,
)
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions as core_exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.api import monitored_resource_pb2  # type: ignore
from google.cloud.logging_v2.services.logging_service_v2 import pagers
from google.cloud.logging_v2.types import log_entry
from google.cloud.logging_v2.types import logging
from .transports.base import LoggingServiceV2Transport, DEFAULT_CLIENT_INFO
from .transports.grpc_asyncio import LoggingServiceV2GrpcAsyncIOTransport
from .client import LoggingServiceV2Client


class LoggingServiceV2AsyncClient:
    """Service for ingesting and querying logs."""

    _client: LoggingServiceV2Client

    DEFAULT_ENDPOINT = LoggingServiceV2Client.DEFAULT_ENDPOINT
    DEFAULT_MTLS_ENDPOINT = LoggingServiceV2Client.DEFAULT_MTLS_ENDPOINT

    log_path = staticmethod(LoggingServiceV2Client.log_path)
    parse_log_path = staticmethod(LoggingServiceV2Client.parse_log_path)
    common_billing_account_path = staticmethod(
        LoggingServiceV2Client.common_billing_account_path
    )
    parse_common_billing_account_path = staticmethod(
        LoggingServiceV2Client.parse_common_billing_account_path
    )
    common_folder_path = staticmethod(LoggingServiceV2Client.common_folder_path)
    parse_common_folder_path = staticmethod(
        LoggingServiceV2Client.parse_common_folder_path
    )
    common_organization_path = staticmethod(
        LoggingServiceV2Client.common_organization_path
    )
    parse_common_organization_path = staticmethod(
        LoggingServiceV2Client.parse_common_organization_path
    )
    common_project_path = staticmethod(LoggingServiceV2Client.common_project_path)
    parse_common_project_path = staticmethod(
        LoggingServiceV2Client.parse_common_project_path
    )
    common_location_path = staticmethod(LoggingServiceV2Client.common_location_path)
    parse_common_location_path = staticmethod(
        LoggingServiceV2Client.parse_common_location_path
    )

    @classmethod
    def from_service_account_info(cls, info: dict, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            info.

        Args:
            info (dict): The service account private key info.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            LoggingServiceV2AsyncClient: The constructed client.
        """
        return LoggingServiceV2Client.from_service_account_info.__func__(LoggingServiceV2AsyncClient, info, *args, **kwargs)  # type: ignore

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
            file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            LoggingServiceV2AsyncClient: The constructed client.
        """
        return LoggingServiceV2Client.from_service_account_file.__func__(LoggingServiceV2AsyncClient, filename, *args, **kwargs)  # type: ignore

    from_service_account_json = from_service_account_file

    @property
    def transport(self) -> LoggingServiceV2Transport:
        """Returns the transport used by the client instance.

        Returns:
            LoggingServiceV2Transport: The transport used by the client instance.
        """
        return self._client.transport

    get_transport_class = functools.partial(
        type(LoggingServiceV2Client).get_transport_class, type(LoggingServiceV2Client)
    )

    def __init__(
        self,
        *,
        credentials: ga_credentials.Credentials = None,
        transport: Union[str, LoggingServiceV2Transport] = "grpc_asyncio",
        client_options: ClientOptions = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
    ) -> None:
        """Instantiates the logging service v2 client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.LoggingServiceV2Transport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS_ENDPOINT
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint) and "auto" (auto switch to the
                default mTLS endpoint if client certificate is present, this is
                the default value). However, the ``api_endpoint`` property takes
                precedence if provided.
                (2) If GOOGLE_API_USE_CLIENT_CERTIFICATE environment variable
                is "true", then the ``client_cert_source`` property can be used
                to provide client certificate for mutual TLS transport. If
                not provided, the default SSL client certificate will be used if
                present. If GOOGLE_API_USE_CLIENT_CERTIFICATE is "false" or not
                set, no client certificate will be used.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        self._client = LoggingServiceV2Client(
            credentials=credentials,
            transport=transport,
            client_options=client_options,
            client_info=client_info,
        )

    async def delete_log(
        self,
        request: logging.DeleteLogRequest = None,
        *,
        log_name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes all the log entries in a log. The log
        reappears if it receives new entries. Log entries
        written shortly before the delete operation might not be
        deleted. Entries received after the delete operation
        with a timestamp before the operation will be deleted.

        Args:
            request (:class:`google.cloud.logging_v2.types.DeleteLogRequest`):
                The request object. The parameters to DeleteLog.
            log_name (:class:`str`):
                Required. The resource name of the log to delete:

                ::

                    "projects/[PROJECT_ID]/logs/[LOG_ID]"
                    "organizations/[ORGANIZATION_ID]/logs/[LOG_ID]"
                    "billingAccounts/[BILLING_ACCOUNT_ID]/logs/[LOG_ID]"
                    "folders/[FOLDER_ID]/logs/[LOG_ID]"

                ``[LOG_ID]`` must be URL-encoded. For example,
                ``"projects/my-project-id/logs/syslog"``,
                ``"organizations/1234567890/logs/cloudresourcemanager.googleapis.com%2Factivity"``.
                For more information about log names, see
                [LogEntry][google.logging.v2.LogEntry].

                This corresponds to the ``log_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([log_name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = logging.DeleteLogRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if log_name is not None:
            request.log_name = log_name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.delete_log,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.InternalServerError,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("log_name", request.log_name),)),
        )

        # Send the request.
        await rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    async def write_log_entries(
        self,
        request: logging.WriteLogEntriesRequest = None,
        *,
        log_name: str = None,
        resource: monitored_resource_pb2.MonitoredResource = None,
        labels: Sequence[logging.WriteLogEntriesRequest.LabelsEntry] = None,
        entries: Sequence[log_entry.LogEntry] = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> logging.WriteLogEntriesResponse:
        r"""Writes log entries to Logging. This API method is the
        only way to send log entries to Logging. This method is
        used, directly or indirectly, by the Logging agent
        (fluentd) and all logging libraries configured to use
        Logging. A single request may contain log entries for a
        maximum of 1000 different resources (projects,
        organizations, billing accounts or folders)

        Args:
            request (:class:`google.cloud.logging_v2.types.WriteLogEntriesRequest`):
                The request object. The parameters to WriteLogEntries.
            log_name (:class:`str`):
                Optional. A default log resource name that is assigned
                to all log entries in ``entries`` that do not specify a
                value for ``log_name``:

                ::

                    "projects/[PROJECT_ID]/logs/[LOG_ID]"
                    "organizations/[ORGANIZATION_ID]/logs/[LOG_ID]"
                    "billingAccounts/[BILLING_ACCOUNT_ID]/logs/[LOG_ID]"
                    "folders/[FOLDER_ID]/logs/[LOG_ID]"

                ``[LOG_ID]`` must be URL-encoded. For example:

                ::

                    "projects/my-project-id/logs/syslog"
                    "organizations/1234567890/logs/cloudresourcemanager.googleapis.com%2Factivity"

                The permission ``logging.logEntries.create`` is needed
                on each project, organization, billing account, or
                folder that is receiving new log entries, whether the
                resource is specified in ``logName`` or in an individual
                log entry.

                This corresponds to the ``log_name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            resource (:class:`google.api.monitored_resource_pb2.MonitoredResource`):
                Optional. A default monitored resource object that is
                assigned to all log entries in ``entries`` that do not
                specify a value for ``resource``. Example:

                ::

                    { "type": "gce_instance",
                      "labels": {
                        "zone": "us-central1-a", "instance_id": "00000000000000000000" }}

                See [LogEntry][google.logging.v2.LogEntry].

                This corresponds to the ``resource`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            labels (:class:`Sequence[google.cloud.logging_v2.types.WriteLogEntriesRequest.LabelsEntry]`):
                Optional. Default labels that are added to the
                ``labels`` field of all log entries in ``entries``. If a
                log entry already has a label with the same key as a
                label in this parameter, then the log entry's label is
                not changed. See [LogEntry][google.logging.v2.LogEntry].

                This corresponds to the ``labels`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            entries (:class:`Sequence[google.cloud.logging_v2.types.LogEntry]`):
                Required. The log entries to send to Logging. The order
                of log entries in this list does not matter. Values
                supplied in this method's ``log_name``, ``resource``,
                and ``labels`` fields are copied into those log entries
                in this list that do not include values for their
                corresponding fields. For more information, see the
                [LogEntry][google.logging.v2.LogEntry] type.

                If the ``timestamp`` or ``insert_id`` fields are missing
                in log entries, then this method supplies the current
                time or a unique identifier, respectively. The supplied
                values are chosen so that, among the log entries that
                did not supply their own values, the entries earlier in
                the list will sort before the entries later in the list.
                See the ``entries.list`` method.

                Log entries with timestamps that are more than the `logs
                retention
                period <https://cloud.google.com/logging/quota-policy>`__
                in the past or more than 24 hours in the future will not
                be available when calling ``entries.list``. However,
                those log entries can still be `exported with
                LogSinks <https://cloud.google.com/logging/docs/api/tasks/exporting-logs>`__.

                To improve throughput and to avoid exceeding the `quota
                limit <https://cloud.google.com/logging/quota-policy>`__
                for calls to ``entries.write``, you should try to
                include several log entries in this list, rather than
                calling this method for each individual log entry.

                This corresponds to the ``entries`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.logging_v2.types.WriteLogEntriesResponse:
                Result returned from WriteLogEntries.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([log_name, resource, labels, entries])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = logging.WriteLogEntriesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if log_name is not None:
            request.log_name = log_name
        if resource is not None:
            request.resource = resource

        if labels:
            request.labels.update(labels)
        if entries:
            request.entries.extend(entries)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.write_log_entries,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.InternalServerError,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    async def list_log_entries(
        self,
        request: logging.ListLogEntriesRequest = None,
        *,
        resource_names: Sequence[str] = None,
        filter: str = None,
        order_by: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListLogEntriesAsyncPager:
        r"""Lists log entries. Use this method to retrieve log entries that
        originated from a project/folder/organization/billing account.
        For ways to export log entries, see `Exporting
        Logs <https://cloud.google.com/logging/docs/export>`__.

        Args:
            request (:class:`google.cloud.logging_v2.types.ListLogEntriesRequest`):
                The request object. The parameters to `ListLogEntries`.
            resource_names (:class:`Sequence[str]`):
                Required. Names of one or more parent resources from
                which to retrieve log entries:

                ::

                    "projects/[PROJECT_ID]"
                    "organizations/[ORGANIZATION_ID]"
                    "billingAccounts/[BILLING_ACCOUNT_ID]"
                    "folders/[FOLDER_ID]"

                May alternatively be one or more views
                projects/[PROJECT_ID]/locations/[LOCATION_ID]/buckets/[BUCKET_ID]/views/[VIEW_ID]
                organization/[ORGANIZATION_ID]/locations/[LOCATION_ID]/buckets/[BUCKET_ID]/views/[VIEW_ID]
                billingAccounts/[BILLING_ACCOUNT_ID]/locations/[LOCATION_ID]/buckets/[BUCKET_ID]/views/[VIEW_ID]
                folders/[FOLDER_ID]/locations/[LOCATION_ID]/buckets/[BUCKET_ID]/views/[VIEW_ID]

                Projects listed in the ``project_ids`` field are added
                to this list.

                This corresponds to the ``resource_names`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            filter (:class:`str`):
                Optional. A filter that chooses which log entries to
                return. See `Advanced Logs
                Queries <https://cloud.google.com/logging/docs/view/advanced-queries>`__.
                Only log entries that match the filter are returned. An
                empty filter matches all log entries in the resources
                listed in ``resource_names``. Referencing a parent
                resource that is not listed in ``resource_names`` will
                cause the filter to return no results. The maximum
                length of the filter is 20000 characters.

                This corresponds to the ``filter`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            order_by (:class:`str`):
                Optional. How the results should be sorted. Presently,
                the only permitted values are ``"timestamp asc"``
                (default) and ``"timestamp desc"``. The first option
                returns entries in order of increasing values of
                ``LogEntry.timestamp`` (oldest first), and the second
                option returns entries in order of decreasing timestamps
                (newest first). Entries with equal timestamps are
                returned in order of their ``insert_id`` values.

                This corresponds to the ``order_by`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.logging_v2.services.logging_service_v2.pagers.ListLogEntriesAsyncPager:
                Result returned from ListLogEntries.

                Iterating over this object will yield results and
                resolve additional pages automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([resource_names, filter, order_by])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = logging.ListLogEntriesRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if filter is not None:
            request.filter = filter
        if order_by is not None:
            request.order_by = order_by
        if resource_names:
            request.resource_names.extend(resource_names)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_log_entries,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.InternalServerError,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListLogEntriesAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_monitored_resource_descriptors(
        self,
        request: logging.ListMonitoredResourceDescriptorsRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListMonitoredResourceDescriptorsAsyncPager:
        r"""Lists the descriptors for monitored resource types
        used by Logging.

        Args:
            request (:class:`google.cloud.logging_v2.types.ListMonitoredResourceDescriptorsRequest`):
                The request object. The parameters to
                ListMonitoredResourceDescriptors
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.logging_v2.services.logging_service_v2.pagers.ListMonitoredResourceDescriptorsAsyncPager:
                Result returned from
                ListMonitoredResourceDescriptors.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        request = logging.ListMonitoredResourceDescriptorsRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_monitored_resource_descriptors,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.InternalServerError,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListMonitoredResourceDescriptorsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    async def list_logs(
        self,
        request: logging.ListLogsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListLogsAsyncPager:
        r"""Lists the logs in projects, organizations, folders,
        or billing accounts. Only logs that have entries are
        listed.

        Args:
            request (:class:`google.cloud.logging_v2.types.ListLogsRequest`):
                The request object. The parameters to ListLogs.
            parent (:class:`str`):
                Required. The resource name that owns the logs:

                ::

                    "projects/[PROJECT_ID]"
                    "organizations/[ORGANIZATION_ID]"
                    "billingAccounts/[BILLING_ACCOUNT_ID]"
                    "folders/[FOLDER_ID]"

                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            google.cloud.logging_v2.services.logging_service_v2.pagers.ListLogsAsyncPager:
                Result returned from ListLogs.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        request = logging.ListLogsRequest(request)

        # If we have keyword arguments corresponding to fields on the
        # request, apply these.
        if parent is not None:
            request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.list_logs,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.InternalServerError,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=60.0,
            ),
            default_timeout=60.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = await rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__aiter__` convenience method.
        response = pagers.ListLogsAsyncPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def tail_log_entries(
        self,
        requests: AsyncIterator[logging.TailLogEntriesRequest] = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> Awaitable[AsyncIterable[logging.TailLogEntriesResponse]]:
        r"""Streaming read of log entries as they are ingested.
        Until the stream is terminated, it will continue reading
        logs.

        Args:
            requests (AsyncIterator[`google.cloud.logging_v2.types.TailLogEntriesRequest`]):
                The request object AsyncIterator. The parameters to `TailLogEntries`.
            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            AsyncIterable[google.cloud.logging_v2.types.TailLogEntriesResponse]:
                Result returned from TailLogEntries.
        """

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = gapic_v1.method_async.wrap_method(
            self._client._transport.tail_log_entries,
            default_retry=retries.Retry(
                initial=0.1,
                maximum=60.0,
                multiplier=1.3,
                predicate=retries.if_exception_type(
                    core_exceptions.DeadlineExceeded,
                    core_exceptions.InternalServerError,
                    core_exceptions.ServiceUnavailable,
                ),
                deadline=3600.0,
            ),
            default_timeout=3600.0,
            client_info=DEFAULT_CLIENT_INFO,
        )

        # Send the request.
        response = rpc(requests, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response


try:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-logging",).version,
    )
except pkg_resources.DistributionNotFound:
    DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo()


__all__ = ("LoggingServiceV2AsyncClient",)
