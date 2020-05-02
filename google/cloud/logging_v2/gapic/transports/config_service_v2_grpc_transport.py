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


import google.api_core.grpc_helpers

from google.cloud.logging_v2.proto import logging_config_pb2_grpc


class ConfigServiceV2GrpcTransport(object):
    """gRPC transport class providing stubs for
    google.logging.v2 ConfigServiceV2 API.

    The transport provides access to the raw gRPC stubs,
    which can be used to take advantage of advanced
    features of gRPC.
    """

    # The scopes needed to make gRPC calls to all of the methods defined
    # in this service.
    _OAUTH_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
        "https://www.googleapis.com/auth/cloud-platform.read-only",
        "https://www.googleapis.com/auth/logging.admin",
        "https://www.googleapis.com/auth/logging.read",
        "https://www.googleapis.com/auth/logging.write",
    )

    def __init__(
        self, channel=None, credentials=None, address="logging.googleapis.com:443"
    ):
        """Instantiate the transport class.

        Args:
            channel (grpc.Channel): A ``Channel`` instance through
                which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            address (str): The address where the service is hosted.
        """
        # If both `channel` and `credentials` are specified, raise an
        # exception (channels come with credentials baked in already).
        if channel is not None and credentials is not None:
            raise ValueError(
                "The `channel` and `credentials` arguments are mutually " "exclusive.",
            )

        # Create the channel.
        if channel is None:
            channel = self.create_channel(
                address=address,
                credentials=credentials,
                options={
                    "grpc.max_send_message_length": -1,
                    "grpc.max_receive_message_length": -1,
                }.items(),
            )

        self._channel = channel

        # gRPC uses objects called "stubs" that are bound to the
        # channel and provide a basic method for each RPC.
        self._stubs = {
            "config_service_v2_stub": logging_config_pb2_grpc.ConfigServiceV2Stub(
                channel
            ),
        }

    @classmethod
    def create_channel(
        cls, address="logging.googleapis.com:443", credentials=None, **kwargs
    ):
        """Create and return a gRPC channel object.

        Args:
            address (str): The host for the channel to use.
            credentials (~.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            kwargs (dict): Keyword arguments, which are passed to the
                channel creation.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return google.api_core.grpc_helpers.create_channel(
            address, credentials=credentials, scopes=cls._OAUTH_SCOPES, **kwargs
        )

    @property
    def channel(self):
        """The gRPC channel used by the transport.

        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return self._channel

    @property
    def list_buckets(self):
        """Return the gRPC stub for :meth:`ConfigServiceV2Client.list_buckets`.

        Lists buckets (Beta).

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["config_service_v2_stub"].ListBuckets

    @property
    def get_bucket(self):
        """Return the gRPC stub for :meth:`ConfigServiceV2Client.get_bucket`.

        Gets a bucket (Beta).

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["config_service_v2_stub"].GetBucket

    @property
    def update_bucket(self):
        """Return the gRPC stub for :meth:`ConfigServiceV2Client.update_bucket`.

        Required. A set of labels used to describe instances of this
        monitored resource type. For example, an individual Google Cloud SQL
        database is identified by values for the labels ``"database_id"`` and
        ``"zone"``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["config_service_v2_stub"].UpdateBucket

    @property
    def list_sinks(self):
        """Return the gRPC stub for :meth:`ConfigServiceV2Client.list_sinks`.

        Lists sinks.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["config_service_v2_stub"].ListSinks

    @property
    def get_sink(self):
        """Return the gRPC stub for :meth:`ConfigServiceV2Client.get_sink`.

        Gets a sink.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["config_service_v2_stub"].GetSink

    @property
    def create_sink(self):
        """Return the gRPC stub for :meth:`ConfigServiceV2Client.create_sink`.

        Optional. This field applies only to sinks owned by organizations
        and folders. If the field is false, the default, only the logs owned by
        the sink's parent resource are available for export. If the field is
        true, then logs from all the projects, folders, and billing accounts
        contained in the sink's parent resource are also available for export.
        Whether a particular log entry from the children is exported depends on
        the sink's filter expression. For example, if this field is true, then
        the filter ``resource.type=gce_instance`` would export all Compute
        Engine VM instance log entries from all projects in the sink's parent.
        To only export entries from certain child projects, filter on the
        project part of the log name:

        ::

            logName:("projects/test-project1/" OR "projects/test-project2/") AND
            resource.type=gce_instance

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["config_service_v2_stub"].CreateSink

    @property
    def update_sink(self):
        """Return the gRPC stub for :meth:`ConfigServiceV2Client.update_sink`.

        The parameters to ``UpdateBucket`` (Beta).

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["config_service_v2_stub"].UpdateSink

    @property
    def delete_sink(self):
        """Return the gRPC stub for :meth:`ConfigServiceV2Client.delete_sink`.

        Required. The full resource name of the bucket to update.

        ::

            "projects/[PROJECT_ID]/locations/[LOCATION_ID]/buckets/[BUCKET_ID]"
            "organizations/[ORGANIZATION_ID]/locations/[LOCATION_ID]/buckets/[BUCKET_ID]"
            "billingAccounts/[BILLING_ACCOUNT_ID]/locations/[LOCATION_ID]/buckets/[BUCKET_ID]"
            "folders/[FOLDER_ID]/locations/[LOCATION_ID]/buckets/[BUCKET_ID]"

        Example:
        ``"projects/my-project-id/locations/my-location/buckets/my-bucket-id"``.
        Also requires permission "resourcemanager.projects.updateLiens" to set
        the locked property

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["config_service_v2_stub"].DeleteSink

    @property
    def list_exclusions(self):
        """Return the gRPC stub for :meth:`ConfigServiceV2Client.list_exclusions`.

        Lists all the exclusions in a parent resource.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["config_service_v2_stub"].ListExclusions

    @property
    def get_exclusion(self):
        """Return the gRPC stub for :meth:`ConfigServiceV2Client.get_exclusion`.

        Gets the description of an exclusion.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["config_service_v2_stub"].GetExclusion

    @property
    def create_exclusion(self):
        """Return the gRPC stub for :meth:`ConfigServiceV2Client.create_exclusion`.

        Creates a new exclusion in a specified parent resource.
        Only log entries belonging to that resource can be excluded.
        You can have up to 10 exclusions in a resource.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["config_service_v2_stub"].CreateExclusion

    @property
    def update_exclusion(self):
        """Return the gRPC stub for :meth:`ConfigServiceV2Client.update_exclusion`.

        Changes one or more properties of an existing exclusion.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["config_service_v2_stub"].UpdateExclusion

    @property
    def delete_exclusion(self):
        """Return the gRPC stub for :meth:`ConfigServiceV2Client.delete_exclusion`.

        Deletes an exclusion.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["config_service_v2_stub"].DeleteExclusion

    @property
    def get_cmek_settings(self):
        """Return the gRPC stub for :meth:`ConfigServiceV2Client.get_cmek_settings`.

        A specific metric, identified by specifying values for all of the
        labels of a ``MetricDescriptor``.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["config_service_v2_stub"].GetCmekSettings

    @property
    def update_cmek_settings(self):
        """Return the gRPC stub for :meth:`ConfigServiceV2Client.update_cmek_settings`.

        Creates a sink that exports specified log entries to a destination.
        The export of newly-ingested log entries begins immediately, unless the
        sink's ``writer_identity`` is not permitted to write to the destination.
        A sink can export log entries only from the resource owning the sink.

        Returns:
            Callable: A callable which accepts the appropriate
                deserialized request object and returns a
                deserialized response object.
        """
        return self._stubs["config_service_v2_stub"].UpdateCmekSettings
