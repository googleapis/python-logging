# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.cloud.logging_v2.proto import (
    logging_config_pb2 as google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2,
)
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class ConfigServiceV2Stub(object):
    """Service for configuring sinks used to route log entries.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListBuckets = channel.unary_unary(
            "/google.logging.v2.ConfigServiceV2/ListBuckets",
            request_serializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.ListBucketsRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.ListBucketsResponse.FromString,
        )
        self.GetBucket = channel.unary_unary(
            "/google.logging.v2.ConfigServiceV2/GetBucket",
            request_serializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.GetBucketRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.LogBucket.FromString,
        )
        self.UpdateBucket = channel.unary_unary(
            "/google.logging.v2.ConfigServiceV2/UpdateBucket",
            request_serializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.UpdateBucketRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.LogBucket.FromString,
        )
        self.ListSinks = channel.unary_unary(
            "/google.logging.v2.ConfigServiceV2/ListSinks",
            request_serializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.ListSinksRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.ListSinksResponse.FromString,
        )
        self.GetSink = channel.unary_unary(
            "/google.logging.v2.ConfigServiceV2/GetSink",
            request_serializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.GetSinkRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.LogSink.FromString,
        )
        self.CreateSink = channel.unary_unary(
            "/google.logging.v2.ConfigServiceV2/CreateSink",
            request_serializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.CreateSinkRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.LogSink.FromString,
        )
        self.UpdateSink = channel.unary_unary(
            "/google.logging.v2.ConfigServiceV2/UpdateSink",
            request_serializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.UpdateSinkRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.LogSink.FromString,
        )
        self.DeleteSink = channel.unary_unary(
            "/google.logging.v2.ConfigServiceV2/DeleteSink",
            request_serializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.DeleteSinkRequest.SerializeToString,
            response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
        self.ListExclusions = channel.unary_unary(
            "/google.logging.v2.ConfigServiceV2/ListExclusions",
            request_serializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.ListExclusionsRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.ListExclusionsResponse.FromString,
        )
        self.GetExclusion = channel.unary_unary(
            "/google.logging.v2.ConfigServiceV2/GetExclusion",
            request_serializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.GetExclusionRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.LogExclusion.FromString,
        )
        self.CreateExclusion = channel.unary_unary(
            "/google.logging.v2.ConfigServiceV2/CreateExclusion",
            request_serializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.CreateExclusionRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.LogExclusion.FromString,
        )
        self.UpdateExclusion = channel.unary_unary(
            "/google.logging.v2.ConfigServiceV2/UpdateExclusion",
            request_serializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.UpdateExclusionRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.LogExclusion.FromString,
        )
        self.DeleteExclusion = channel.unary_unary(
            "/google.logging.v2.ConfigServiceV2/DeleteExclusion",
            request_serializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.DeleteExclusionRequest.SerializeToString,
            response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
        self.GetCmekSettings = channel.unary_unary(
            "/google.logging.v2.ConfigServiceV2/GetCmekSettings",
            request_serializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.GetCmekSettingsRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.CmekSettings.FromString,
        )
        self.UpdateCmekSettings = channel.unary_unary(
            "/google.logging.v2.ConfigServiceV2/UpdateCmekSettings",
            request_serializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.UpdateCmekSettingsRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.CmekSettings.FromString,
        )


class ConfigServiceV2Servicer(object):
    """Service for configuring sinks used to route log entries.
    """

    def ListBuckets(self, request, context):
        """Lists buckets (Beta).
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetBucket(self, request, context):
        """Gets a bucket (Beta).
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def UpdateBucket(self, request, context):
        """Updates a bucket. This method replaces the following fields in the
        existing bucket with values from the new bucket: `retention_period`

        If the retention period is decreased and the bucket is locked,
        FAILED_PRECONDITION will be returned.

        If the bucket has a LifecycleState of DELETE_REQUESTED, FAILED_PRECONDITION
        will be returned.

        A buckets region may not be modified after it is created.
        This method is in Beta.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def ListSinks(self, request, context):
        """Lists sinks.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetSink(self, request, context):
        """Gets a sink.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def CreateSink(self, request, context):
        """Creates a sink that exports specified log entries to a destination. The
        export of newly-ingested log entries begins immediately, unless the sink's
        `writer_identity` is not permitted to write to the destination. A sink can
        export log entries only from the resource owning the sink.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def UpdateSink(self, request, context):
        """Updates a sink. This method replaces the following fields in the existing
        sink with values from the new sink: `destination`, and `filter`.

        The updated sink might also have a new `writer_identity`; see the
        `unique_writer_identity` field.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def DeleteSink(self, request, context):
        """Deletes a sink. If the sink has a unique `writer_identity`, then that
        service account is also deleted.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def ListExclusions(self, request, context):
        """Lists all the exclusions in a parent resource.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetExclusion(self, request, context):
        """Gets the description of an exclusion.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def CreateExclusion(self, request, context):
        """Creates a new exclusion in a specified parent resource.
        Only log entries belonging to that resource can be excluded.
        You can have up to 10 exclusions in a resource.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def UpdateExclusion(self, request, context):
        """Changes one or more properties of an existing exclusion.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def DeleteExclusion(self, request, context):
        """Deletes an exclusion.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetCmekSettings(self, request, context):
        """Gets the Logs Router CMEK settings for the given resource.

        Note: CMEK for the Logs Router can currently only be configured for GCP
        organizations. Once configured, it applies to all projects and folders in
        the GCP organization.

        See [Enabling CMEK for Logs
        Router](https://cloud.google.com/logging/docs/routing/managed-encryption)
        for more information.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def UpdateCmekSettings(self, request, context):
        """Updates the Logs Router CMEK settings for the given resource.

        Note: CMEK for the Logs Router can currently only be configured for GCP
        organizations. Once configured, it applies to all projects and folders in
        the GCP organization.

        [UpdateCmekSettings][google.logging.v2.ConfigServiceV2.UpdateCmekSettings]
        will fail if 1) `kms_key_name` is invalid, or 2) the associated service
        account does not have the required
        `roles/cloudkms.cryptoKeyEncrypterDecrypter` role assigned for the key, or
        3) access to the key is disabled.

        See [Enabling CMEK for Logs
        Router](https://cloud.google.com/logging/docs/routing/managed-encryption)
        for more information.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_ConfigServiceV2Servicer_to_server(servicer, server):
    rpc_method_handlers = {
        "ListBuckets": grpc.unary_unary_rpc_method_handler(
            servicer.ListBuckets,
            request_deserializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.ListBucketsRequest.FromString,
            response_serializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.ListBucketsResponse.SerializeToString,
        ),
        "GetBucket": grpc.unary_unary_rpc_method_handler(
            servicer.GetBucket,
            request_deserializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.GetBucketRequest.FromString,
            response_serializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.LogBucket.SerializeToString,
        ),
        "UpdateBucket": grpc.unary_unary_rpc_method_handler(
            servicer.UpdateBucket,
            request_deserializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.UpdateBucketRequest.FromString,
            response_serializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.LogBucket.SerializeToString,
        ),
        "ListSinks": grpc.unary_unary_rpc_method_handler(
            servicer.ListSinks,
            request_deserializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.ListSinksRequest.FromString,
            response_serializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.ListSinksResponse.SerializeToString,
        ),
        "GetSink": grpc.unary_unary_rpc_method_handler(
            servicer.GetSink,
            request_deserializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.GetSinkRequest.FromString,
            response_serializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.LogSink.SerializeToString,
        ),
        "CreateSink": grpc.unary_unary_rpc_method_handler(
            servicer.CreateSink,
            request_deserializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.CreateSinkRequest.FromString,
            response_serializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.LogSink.SerializeToString,
        ),
        "UpdateSink": grpc.unary_unary_rpc_method_handler(
            servicer.UpdateSink,
            request_deserializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.UpdateSinkRequest.FromString,
            response_serializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.LogSink.SerializeToString,
        ),
        "DeleteSink": grpc.unary_unary_rpc_method_handler(
            servicer.DeleteSink,
            request_deserializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.DeleteSinkRequest.FromString,
            response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        ),
        "ListExclusions": grpc.unary_unary_rpc_method_handler(
            servicer.ListExclusions,
            request_deserializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.ListExclusionsRequest.FromString,
            response_serializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.ListExclusionsResponse.SerializeToString,
        ),
        "GetExclusion": grpc.unary_unary_rpc_method_handler(
            servicer.GetExclusion,
            request_deserializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.GetExclusionRequest.FromString,
            response_serializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.LogExclusion.SerializeToString,
        ),
        "CreateExclusion": grpc.unary_unary_rpc_method_handler(
            servicer.CreateExclusion,
            request_deserializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.CreateExclusionRequest.FromString,
            response_serializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.LogExclusion.SerializeToString,
        ),
        "UpdateExclusion": grpc.unary_unary_rpc_method_handler(
            servicer.UpdateExclusion,
            request_deserializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.UpdateExclusionRequest.FromString,
            response_serializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.LogExclusion.SerializeToString,
        ),
        "DeleteExclusion": grpc.unary_unary_rpc_method_handler(
            servicer.DeleteExclusion,
            request_deserializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.DeleteExclusionRequest.FromString,
            response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        ),
        "GetCmekSettings": grpc.unary_unary_rpc_method_handler(
            servicer.GetCmekSettings,
            request_deserializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.GetCmekSettingsRequest.FromString,
            response_serializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.CmekSettings.SerializeToString,
        ),
        "UpdateCmekSettings": grpc.unary_unary_rpc_method_handler(
            servicer.UpdateCmekSettings,
            request_deserializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.UpdateCmekSettingsRequest.FromString,
            response_serializer=google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.CmekSettings.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "google.logging.v2.ConfigServiceV2", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class ConfigServiceV2(object):
    """Service for configuring sinks used to route log entries.
    """

    @staticmethod
    def ListBuckets(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/google.logging.v2.ConfigServiceV2/ListBuckets",
            google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.ListBucketsRequest.SerializeToString,
            google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.ListBucketsResponse.FromString,
            options,
            channel_credentials,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def GetBucket(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/google.logging.v2.ConfigServiceV2/GetBucket",
            google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.GetBucketRequest.SerializeToString,
            google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.LogBucket.FromString,
            options,
            channel_credentials,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def UpdateBucket(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/google.logging.v2.ConfigServiceV2/UpdateBucket",
            google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.UpdateBucketRequest.SerializeToString,
            google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.LogBucket.FromString,
            options,
            channel_credentials,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def ListSinks(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/google.logging.v2.ConfigServiceV2/ListSinks",
            google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.ListSinksRequest.SerializeToString,
            google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.ListSinksResponse.FromString,
            options,
            channel_credentials,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def GetSink(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/google.logging.v2.ConfigServiceV2/GetSink",
            google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.GetSinkRequest.SerializeToString,
            google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.LogSink.FromString,
            options,
            channel_credentials,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def CreateSink(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/google.logging.v2.ConfigServiceV2/CreateSink",
            google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.CreateSinkRequest.SerializeToString,
            google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.LogSink.FromString,
            options,
            channel_credentials,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def UpdateSink(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/google.logging.v2.ConfigServiceV2/UpdateSink",
            google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.UpdateSinkRequest.SerializeToString,
            google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.LogSink.FromString,
            options,
            channel_credentials,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def DeleteSink(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/google.logging.v2.ConfigServiceV2/DeleteSink",
            google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.DeleteSinkRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options,
            channel_credentials,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def ListExclusions(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/google.logging.v2.ConfigServiceV2/ListExclusions",
            google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.ListExclusionsRequest.SerializeToString,
            google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.ListExclusionsResponse.FromString,
            options,
            channel_credentials,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def GetExclusion(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/google.logging.v2.ConfigServiceV2/GetExclusion",
            google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.GetExclusionRequest.SerializeToString,
            google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.LogExclusion.FromString,
            options,
            channel_credentials,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def CreateExclusion(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/google.logging.v2.ConfigServiceV2/CreateExclusion",
            google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.CreateExclusionRequest.SerializeToString,
            google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.LogExclusion.FromString,
            options,
            channel_credentials,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def UpdateExclusion(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/google.logging.v2.ConfigServiceV2/UpdateExclusion",
            google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.UpdateExclusionRequest.SerializeToString,
            google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.LogExclusion.FromString,
            options,
            channel_credentials,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def DeleteExclusion(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/google.logging.v2.ConfigServiceV2/DeleteExclusion",
            google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.DeleteExclusionRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options,
            channel_credentials,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def GetCmekSettings(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/google.logging.v2.ConfigServiceV2/GetCmekSettings",
            google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.GetCmekSettingsRequest.SerializeToString,
            google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.CmekSettings.FromString,
            options,
            channel_credentials,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def UpdateCmekSettings(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/google.logging.v2.ConfigServiceV2/UpdateCmekSettings",
            google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.UpdateCmekSettingsRequest.SerializeToString,
            google_dot_cloud_dot_logging__v2_dot_proto_dot_logging__config__pb2.CmekSettings.FromString,
            options,
            channel_credentials,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
