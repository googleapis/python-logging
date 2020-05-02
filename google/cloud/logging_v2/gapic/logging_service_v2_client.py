# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Accesses the google.logging.v2 LoggingServiceV2 API."""

import functools
import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.page_iterator
import google.api_core.path_template
import grpc

from google.api import monitored_resource_pb2
from google.cloud.logging_v2.gapic import enums
from google.cloud.logging_v2.gapic import logging_service_v2_client_config
from google.cloud.logging_v2.gapic.transports import logging_service_v2_grpc_transport
from google.cloud.logging_v2.proto import log_entry_pb2
from google.cloud.logging_v2.proto import logging_config_pb2
from google.cloud.logging_v2.proto import logging_config_pb2_grpc
from google.cloud.logging_v2.proto import logging_pb2
from google.cloud.logging_v2.proto import logging_pb2_grpc
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-logging",).version


class LoggingServiceV2Client(object):
    """Service for ingesting and querying logs."""

    SERVICE_ADDRESS = "logging.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.logging.v2.LoggingServiceV2"

    @classmethod
    def from_service_account_file(cls, filename, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            LoggingServiceV2Client: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def billing_account_path(cls, billing_account):
        """Return a fully-qualified billing_account string."""
        return google.api_core.path_template.expand(
            "billingAccounts/{billing_account}", billing_account=billing_account,
        )

    @classmethod
    def folder_path(cls, folder):
        """Return a fully-qualified folder string."""
        return google.api_core.path_template.expand("folders/{folder}", folder=folder,)

    @classmethod
    def log_path(cls, project, log):
        """Return a fully-qualified log string."""
        return google.api_core.path_template.expand(
            "projects/{project}/logs/{log}", project=project, log=log,
        )

    @classmethod
    def organization_path(cls, organization):
        """Return a fully-qualified organization string."""
        return google.api_core.path_template.expand(
            "organizations/{organization}", organization=organization,
        )

    @classmethod
    def project_path(cls, project):
        """Return a fully-qualified project string."""
        return google.api_core.path_template.expand(
            "projects/{project}", project=project,
        )

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
        client_options=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.LoggingServiceV2GrpcTransport,
                    Callable[[~.Credentials, type], ~.LoggingServiceV2GrpcTransport]): A transport
                instance, responsible for actually making the API calls.
                The default transport uses the gRPC protocol.
                This argument may also be a callable which returns a
                transport instance. Callables will be sent the credentials
                as the first argument and the default transport class as
                the second argument.
            channel (grpc.Channel): DEPRECATED. A ``Channel`` instance
                through which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is mutually exclusive with providing a
                transport instance to ``transport``; doing so will raise
                an exception.
            client_config (dict): DEPRECATED. A dictionary of call options for
                each method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            client_options (Union[dict, google.api_core.client_options.ClientOptions]):
                Client options used to set user options on the client. API Endpoint
                should be set through client_options.
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = logging_service_v2_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        api_endpoint = self.SERVICE_ADDRESS
        if client_options:
            if type(client_options) == dict:
                client_options = google.api_core.client_options.from_dict(
                    client_options
                )
            if client_options.api_endpoint:
                api_endpoint = client_options.api_endpoint

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=logging_service_v2_grpc_transport.LoggingServiceV2GrpcTransport,
                    address=api_endpoint,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = logging_service_v2_grpc_transport.LoggingServiceV2GrpcTransport(
                address=api_endpoint, channel=channel, credentials=credentials,
            )

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=_GAPIC_LIBRARY_VERSION,
            )
        else:
            client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config["interfaces"][self._INTERFACE_NAME],
        )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def write_log_entries(
        self,
        entries,
        log_name=None,
        resource=None,
        labels=None,
        partial_success=None,
        dry_run=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Writes log entries to Logging. This API method is the
        only way to send log entries to Logging. This method
        is used, directly or indirectly, by the Logging agent
        (fluentd) and all logging libraries configured to use Logging.
        A single request may contain log entries for a maximum of 1000
        different resources (projects, organizations, billing accounts or
        folders)

        Example:
            >>> from google.cloud import logging_v2
            >>>
            >>> client = logging_v2.LoggingServiceV2Client()
            >>>
            >>> # TODO: Initialize `entries`:
            >>> entries = []
            >>>
            >>> response = client.write_log_entries(entries)

        Args:
            entries (list[Union[dict, ~google.cloud.logging_v2.types.LogEntry]]): The number of values in each bucket of the histogram, as described
                in ``bucket_options``. If the distribution does not have a histogram,
                then omit this field. If there is a histogram, then the sum of the
                values in ``bucket_counts`` must equal the value in the ``count`` field
                of the distribution.

                If present, ``bucket_counts`` should contain N values, where N is the
                number of buckets specified in ``bucket_options``. If you supply fewer
                than N values, the remaining values are assumed to be 0.

                The order of the values in ``bucket_counts`` follows the bucket
                numbering schemes described for the three bucket types. The first value
                must be the count for the underflow bucket (number 0). The next N-2
                values are the counts for the finite buckets (number 1 through N-2). The
                N'th value in ``bucket_counts`` is the count for the overflow bucket
                (number N-1).

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.logging_v2.types.LogEntry`
            log_name (str): The resource name of the bucket. For example:
                "projects/my-project-id/locations/my-location/buckets/my-bucket-id The
                supported locations are: "global" "us-central1"

                For the location of ``global`` it is unspecified where logs are actually
                stored. Once a bucket has been created, the location can not be changed.
            resource (Union[dict, ~google.cloud.logging_v2.types.MonitoredResource]): ``FieldMask`` represents a set of symbolic field paths, for example:

                ::

                    paths: "f.a"
                    paths: "f.b.d"

                Here ``f`` represents a field in some root message, ``a`` and ``b``
                fields in the message found in ``f``, and ``d`` a field found in the
                message in ``f.b``.

                Field masks are used to specify a subset of fields that should be
                returned by a get operation or modified by an update operation. Field
                masks also have a custom JSON encoding (see below).

                # Field Masks in Projections

                When used in the context of a projection, a response message or
                sub-message is filtered by the API to only contain those fields as
                specified in the mask. For example, if the mask in the previous example
                is applied to a response message as follows:

                ::

                    f {
                      a : 22
                      b {
                        d : 1
                        x : 2
                      }
                      y : 13
                    }
                    z: 8

                The result will not contain specific values for fields x,y and z (their
                value will be set to the default, and omitted in proto text output):

                ::

                    f {
                      a : 22
                      b {
                        d : 1
                      }
                    }

                A repeated field is not allowed except at the last position of a paths
                string.

                If a FieldMask object is not present in a get operation, the operation
                applies to all fields (as if a FieldMask of all fields had been
                specified).

                Note that a field mask does not necessarily apply to the top-level
                response message. In case of a REST get operation, the field mask
                applies directly to the response, but in case of a REST list operation,
                the mask instead applies to each individual message in the returned
                resource list. In case of a REST custom method, other definitions may be
                used. Where the mask applies will be clearly documented together with
                its declaration in the API. In any case, the effect on the returned
                resource/resources is required behavior for APIs.

                # Field Masks in Update Operations

                A field mask in update operations specifies which fields of the targeted
                resource are going to be updated. The API is required to only change the
                values of the fields as specified in the mask and leave the others
                untouched. If a resource is passed in to describe the updated values,
                the API ignores the values of all fields not covered by the mask.

                If a repeated field is specified for an update operation, new values
                will be appended to the existing repeated field in the target resource.
                Note that a repeated field is only allowed in the last position of a
                ``paths`` string.

                If a sub-message is specified in the last position of the field mask for
                an update operation, then new value will be merged into the existing
                sub-message in the target resource.

                For example, given the target message:

                ::

                    f {
                      b {
                        d: 1
                        x: 2
                      }
                      c: [1]
                    }

                And an update message:

                ::

                    f {
                      b {
                        d: 10
                      }
                      c: [2]
                    }

                then if the field mask is:

                paths: ["f.b", "f.c"]

                then the result will be:

                ::

                    f {
                      b {
                        d: 10
                        x: 2
                      }
                      c: [1, 2]
                    }

                An implementation may provide options to override this default behavior
                for repeated and message fields.

                In order to reset a field's value to the default, the field must be in
                the mask and set to the default value in the provided resource. Hence,
                in order to reset all fields of a resource, provide a default instance
                of the resource and set all fields in the mask, or do not provide a mask
                as described below.

                If a field mask is not present on update, the operation applies to all
                fields (as if a field mask of all fields has been specified). Note that
                in the presence of schema evolution, this may mean that fields the
                client does not know and has therefore not filled into the request will
                be reset to their default. If this is unwanted behavior, a specific
                service may require a client to always specify a field mask, producing
                an error if not.

                As with get operations, the location of the resource which describes the
                updated values in the request message depends on the operation kind. In
                any case, the effect of the field mask is required to be honored by the
                API.

                ## Considerations for HTTP REST

                The HTTP kind of an update operation which uses a field mask must be set
                to PATCH instead of PUT in order to satisfy HTTP semantics (PUT must
                only be used for full updates).

                # JSON Encoding of Field Masks

                In JSON, a field mask is encoded as a single string where paths are
                separated by a comma. Fields name in each path are converted to/from
                lower-camel naming conventions.

                As an example, consider the following message declarations:

                ::

                    message Profile {
                      User user = 1;
                      Photo photo = 2;
                    }
                    message User {
                      string display_name = 1;
                      string address = 2;
                    }

                In proto a field mask for ``Profile`` may look as such:

                ::

                    mask {
                      paths: "user.display_name"
                      paths: "photo"
                    }

                In JSON, the same mask is represented as below:

                ::

                    {
                      mask: "user.displayName,photo"
                    }

                # Field Masks and Oneof Fields

                Field masks treat fields in oneofs just as regular fields. Consider the
                following message:

                ::

                    message SampleMessage {
                      oneof test_oneof {
                        string name = 4;
                        SubMessage sub_message = 9;
                      }
                    }

                The field mask can be:

                ::

                    mask {
                      paths: "name"
                    }

                Or:

                ::

                    mask {
                      paths: "sub_message"
                    }

                Note that oneof type names ("test_oneof" in this case) cannot be used in
                paths.

                ## Field Mask Verification

                The implementation of any API method which has a FieldMask type field in
                the request should verify the included field paths, and return an
                ``INVALID_ARGUMENT`` error if any path is unmappable.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.logging_v2.types.MonitoredResource`
            labels (dict[str -> str]): Optional. Determines the kind of IAM identity returned as
                ``writer_identity`` in the new sink. If this value is omitted or set to
                false, and if the sink's parent is a project, then the value returned as
                ``writer_identity`` is the same group or service account used by Logging
                before the addition of writer identities to this API. The sink's
                destination must be in the same project as the sink itself.

                If this field is set to true, or if the sink is owned by a non-project
                resource such as an organization, then the value of ``writer_identity``
                will be a unique service account used only for exports from the new
                sink. For more information, see ``writer_identity`` in ``LogSink``.
            partial_success (bool): Optional. The sampling decision of the trace associated with the log
                entry.

                True means that the trace resource name in the ``trace`` field was
                sampled for storage in a trace backend. False means that the trace was
                not sampled for storage when this log entry was written, or the sampling
                decision was unknown at the time. A non-sampled ``trace`` value is still
                useful as a request correlation identifier. The default is False.
            dry_run (bool): Optional. If true, the request should expect normal response, but the
                entries won't be persisted nor exported. Useful for checking whether the
                logging API endpoints are working properly before sending valuable data.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.logging_v2.types.WriteLogEntriesResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "write_log_entries" not in self._inner_api_calls:
            self._inner_api_calls[
                "write_log_entries"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.write_log_entries,
                default_retry=self._method_configs["WriteLogEntries"].retry,
                default_timeout=self._method_configs["WriteLogEntries"].timeout,
                client_info=self._client_info,
            )

        request = logging_pb2.WriteLogEntriesRequest(
            entries=entries,
            log_name=log_name,
            resource=resource,
            labels=labels,
            partial_success=partial_success,
            dry_run=dry_run,
        )
        return self._inner_api_calls["write_log_entries"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def delete_log(
        self,
        log_name,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Deletes all the log entries in a log. The log reappears if it receives new
        entries. Log entries written shortly before the delete operation might not
        be deleted. Entries received after the delete operation with a timestamp
        before the operation will be deleted.

        Example:
            >>> from google.cloud import logging_v2
            >>>
            >>> client = logging_v2.LoggingServiceV2Client()
            >>>
            >>> # TODO: Initialize `log_name`:
            >>> log_name = ''
            >>>
            >>> client.delete_log(log_name)

        Args:
            log_name (str): The severity of the event described in a log entry, expressed as one
                of the standard severity levels listed below. For your reference, the
                levels are assigned the listed numeric values. The effect of using
                numeric values other than those listed is undefined.

                You can filter for log entries by severity. For example, the following
                filter expression will match log entries with severities ``INFO``,
                ``NOTICE``, and ``WARNING``:

                ::

                    severity > DEBUG AND severity <= WARNING

                If you are writing log entries, you should map other severity encodings
                to one of these standard levels. For example, you might map all of
                Java's FINE, FINER, and FINEST levels to ``LogSeverity.DEBUG``. You can
                preserve the original severity level in the log entry payload if you
                wish.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "delete_log" not in self._inner_api_calls:
            self._inner_api_calls[
                "delete_log"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.delete_log,
                default_retry=self._method_configs["DeleteLog"].retry,
                default_timeout=self._method_configs["DeleteLog"].timeout,
                client_info=self._client_info,
            )

        request = logging_pb2.DeleteLogRequest(log_name=log_name,)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("log_name", log_name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        self._inner_api_calls["delete_log"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def list_log_entries(
        self,
        resource_names,
        filter_=None,
        order_by=None,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Signed fractions of a second at nanosecond resolution of the span of
        time. Durations less than one second are represented with a 0
        ``seconds`` field and a positive or negative ``nanos`` field. For
        durations of one second or more, a non-zero value for the ``nanos``
        field must be of the same sign as the ``seconds`` field. Must be from
        -999,999,999 to +999,999,999 inclusive.

        Example:
            >>> from google.cloud import logging_v2
            >>>
            >>> client = logging_v2.LoggingServiceV2Client()
            >>>
            >>> # TODO: Initialize `resource_names`:
            >>> resource_names = []
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_log_entries(resource_names):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_log_entries(resource_names).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            resource_names (list[str]): The parameters to ``UpdateSink``.
            filter_ (str): Optional. The severity of the log entry. The default value is
                ``LogSeverity.DEFAULT``.
            order_by (str): The plural name used in the resource name, such as 'projects' for
                the name of 'projects/{project}'. It is the same concept of the
                ``plural`` field in k8s CRD spec
                https://kubernetes.io/docs/tasks/access-kubernetes-api/custom-resources/custom-resource-definitions/
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.logging_v2.types.LogEntry` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_log_entries" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_log_entries"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_log_entries,
                default_retry=self._method_configs["ListLogEntries"].retry,
                default_timeout=self._method_configs["ListLogEntries"].timeout,
                client_info=self._client_info,
            )

        request = logging_pb2.ListLogEntriesRequest(
            resource_names=resource_names,
            filter=filter_,
            order_by=order_by,
            page_size=page_size,
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_log_entries"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="entries",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def list_monitored_resource_descriptors(
        self,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists the descriptors for monitored resource types used by Logging.

        Example:
            >>> from google.cloud import logging_v2
            >>>
            >>> client = logging_v2.LoggingServiceV2Client()
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_monitored_resource_descriptors():
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_monitored_resource_descriptors().pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`~google.cloud.logging_v2.types.MonitoredResourceDescriptor` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_monitored_resource_descriptors" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_monitored_resource_descriptors"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_monitored_resource_descriptors,
                default_retry=self._method_configs[
                    "ListMonitoredResourceDescriptors"
                ].retry,
                default_timeout=self._method_configs[
                    "ListMonitoredResourceDescriptors"
                ].timeout,
                client_info=self._client_info,
            )

        request = logging_pb2.ListMonitoredResourceDescriptorsRequest(
            page_size=page_size,
        )
        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_monitored_resource_descriptors"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="resource_descriptors",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator

    def list_logs(
        self,
        parent,
        page_size=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Lists the logs in projects, organizations, folders, or billing accounts.
        Only logs that have entries are listed.

        Example:
            >>> from google.cloud import logging_v2
            >>>
            >>> client = logging_v2.LoggingServiceV2Client()
            >>>
            >>> parent = client.project_path('[PROJECT]')
            >>>
            >>> # Iterate over all results
            >>> for element in client.list_logs(parent):
            ...     # process element
            ...     pass
            >>>
            >>>
            >>> # Alternatively:
            >>>
            >>> # Iterate over results one page at a time
            >>> for page in client.list_logs(parent).pages:
            ...     for element in page:
            ...         # process element
            ...         pass

        Args:
            parent (str): See ``HttpRule``.
            page_size (int): The maximum number of resources contained in the
                underlying API response. If page streaming is performed per-
                resource, this parameter does not affect the return value. If page
                streaming is performed per-page, this determines the maximum number
                of resources in a page.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.api_core.page_iterator.PageIterator` instance.
            An iterable of :class:`str` instances.
            You can also iterate over the pages of the response
            using its `pages` property.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "list_logs" not in self._inner_api_calls:
            self._inner_api_calls[
                "list_logs"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.list_logs,
                default_retry=self._method_configs["ListLogs"].retry,
                default_timeout=self._method_configs["ListLogs"].timeout,
                client_info=self._client_info,
            )

        request = logging_pb2.ListLogsRequest(parent=parent, page_size=page_size,)
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("parent", parent)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        iterator = google.api_core.page_iterator.GRPCIterator(
            client=None,
            method=functools.partial(
                self._inner_api_calls["list_logs"],
                retry=retry,
                timeout=timeout,
                metadata=metadata,
            ),
            request=request,
            items_field="log_names",
            request_token_field="page_token",
            response_token_field="next_page_token",
        )
        return iterator
