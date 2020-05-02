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

"""Wrappers for protocol buffer enum types."""

import enum


class LaunchStage(enum.IntEnum):
    """
    Optional. If present, then retrieve the next batch of results from
    the preceding call to this method. ``pageToken`` must be the value of
    ``nextPageToken`` from the previous response. The values of other method
    parameters should be identical to those in the previous call.

    Attributes:
      LAUNCH_STAGE_UNSPECIFIED (int): Do not use this default value.
      EARLY_ACCESS (int): Early Access features are limited to a closed group of testers. To use
      these features, you must sign up in advance and sign a Trusted Tester
      agreement (which includes confidentiality provisions). These features may
      be unstable, changed in backward-incompatible ways, and are not
      guaranteed to be released.
      ALPHA (int): Alpha is a limited availability test for releases before they are cleared
      for widespread use. By Alpha, all significant design issues are resolved
      and we are in the process of verifying functionality. Alpha customers
      need to apply for access, agree to applicable terms, and have their
      projects whitelisted. Alpha releases don’t have to be feature complete,
      no SLAs are provided, and there are no technical support obligations, but
      they will be far enough along that customers can actually use them in
      test environments or for limited-use tests -- just like they would in
      normal production cases.
      BETA (int): Beta is the point at which we are ready to open a release for any
      customer to use. There are no SLA or technical support obligations in a
      Beta release. Products will be complete from a feature perspective, but
      may have some open outstanding issues. Beta releases are suitable for
      limited production use cases.
      GA (int): GA features are open to all developers and are considered stable and
      fully qualified for production use.
      DEPRECATED (int): JSON name of this field. The value is set by protocol compiler. If
      the user has set a "json_name" option on this field, that option's value
      will be used. Otherwise, it's deduced from the field's name by
      converting it to camelCase.
    """

    LAUNCH_STAGE_UNSPECIFIED = 0
    EARLY_ACCESS = 1
    ALPHA = 2
    BETA = 3
    GA = 4
    DEPRECATED = 5


class LifecycleState(enum.IntEnum):
    """
    LogBucket lifecycle states (Beta).

    Attributes:
      LIFECYCLE_STATE_UNSPECIFIED (int): Unspecified state.  This is only used/useful for distinguishing
      unset values.
      ACTIVE (int): The normal and active state.
      DELETE_REQUESTED (int): The bucket has been marked for deletion by the user.
    """

    LIFECYCLE_STATE_UNSPECIFIED = 0
    ACTIVE = 1
    DELETE_REQUESTED = 2


class LogSeverity(enum.IntEnum):
    """
    Required. The resource name of the log to which this log entry
    belongs:

    ::

        "projects/[PROJECT_ID]/logs/[LOG_ID]"
        "organizations/[ORGANIZATION_ID]/logs/[LOG_ID]"
        "billingAccounts/[BILLING_ACCOUNT_ID]/logs/[LOG_ID]"
        "folders/[FOLDER_ID]/logs/[LOG_ID]"

    A project number may be used in place of PROJECT_ID. The project number
    is translated to its corresponding PROJECT_ID internally and the
    ``log_name`` field will contain PROJECT_ID in queries and exports.

    ``[LOG_ID]`` must be URL-encoded within ``log_name``. Example:
    ``"organizations/1234567890/logs/cloudresourcemanager.googleapis.com%2Factivity"``.
    ``[LOG_ID]`` must be less than 512 characters long and can only include
    the following characters: upper and lower case alphanumeric characters,
    forward-slash, underscore, hyphen, and period.

    For backward compatibility, if ``log_name`` begins with a forward-slash,
    such as ``/projects/...``, then the log entry is ingested as usual but
    the forward-slash is removed. Listing the log entry will not show the
    leading slash and filtering for a log name with a leading slash will
    never return any results.

    Attributes:
      DEFAULT (int): (0) The log entry has no assigned severity level.
      DEBUG (int): (100) Debug or trace information.
      INFO (int): (200) Routine information, such as ongoing status or performance.
      NOTICE (int): (300) Normal but significant events, such as start up, shut down, or
      a configuration change.
      WARNING (int): (400) Warning events might cause problems.
      ERROR (int): (500) Error events are likely to cause problems.
      CRITICAL (int): (600) Critical events cause more severe problems or outages.
      ALERT (int): (700) A person must take an action immediately.
      EMERGENCY (int): (800) One or more systems are unusable.
    """

    DEFAULT = 0
    DEBUG = 100
    INFO = 200
    NOTICE = 300
    WARNING = 400
    ERROR = 500
    CRITICAL = 600
    ALERT = 700
    EMERGENCY = 800


class NullValue(enum.IntEnum):
    """
    The status code, which should be an enum value of
    ``google.rpc.Code``.

    Attributes:
      NULL_VALUE (int): Null value.
    """

    NULL_VALUE = 0


class LabelDescriptor(object):
    class ValueType(enum.IntEnum):
        """
        Value types that can be used as label values.

        Attributes:
          STRING (int): A variable-length string. This is the default.
          BOOL (int): Boolean; true or false.
          INT64 (int): A 64-bit signed integer.
        """

        STRING = 0
        BOOL = 1
        INT64 = 2


class LogMetric(object):
    class ApiVersion(enum.IntEnum):
        """
        Logging API version.

        Attributes:
          V2 (int): Logging API v2.
          V1 (int): Logging API v1.
        """

        V2 = 0
        V1 = 1


class LogSink(object):
    class VersionFormat(enum.IntEnum):
        """
        Available log entry formats. Log entries can be written to
        Logging in either format and can be exported in either format.
        Version 2 is the preferred format.

        Attributes:
          VERSION_FORMAT_UNSPECIFIED (int): An unspecified format version that will default to V2.
          V2 (int): The request method. Examples: ``"GET"``, ``"HEAD"``, ``"PUT"``,
          ``"POST"``.
          V1 (int): Specifies a set of buckets with arbitrary widths.

          There are ``size(bounds) + 1`` (= N) buckets. Bucket ``i`` has the
          following boundaries:

          ::

             Upper bound (0 <= i < N-1):     bounds[i]
             Lower bound (1 <= i < N);       bounds[i - 1]

          The ``bounds`` field must contain at least one element. If ``bounds``
          has only one element, then there are no finite buckets, and that single
          element is the common boundary of the overflow and underflow buckets.
        """

        VERSION_FORMAT_UNSPECIFIED = 0
        V2 = 1
        V1 = 2


class MetricDescriptor(object):
    class MetricKind(enum.IntEnum):
        """
        The kind of measurement. It describes how the data is reported.

        Attributes:
          METRIC_KIND_UNSPECIFIED (int): Do not use this default value.
          GAUGE (int): An instantaneous measurement of a value.
          DELTA (int): The change in a value during a time interval.
          CUMULATIVE (int): A value accumulated over a time interval.  Cumulative
          measurements in a time series should have the same start time
          and increasing end times, until an event resets the cumulative
          value to zero and sets a new start time for the following
          points.
        """

        METRIC_KIND_UNSPECIFIED = 0
        GAUGE = 1
        DELTA = 2
        CUMULATIVE = 3

    class ValueType(enum.IntEnum):
        """
        The value type of a metric.

        Attributes:
          VALUE_TYPE_UNSPECIFIED (int): Do not use this default value.
          BOOL (int): ``LogEntry`` version 2 format.
          INT64 (int): The value is a signed 64-bit integer.
          DOUBLE (int): The value is a double precision floating point number.
          STRING (int): A definition of a client library method signature.

          In client libraries, each proto RPC corresponds to one or more methods
          which the end user is able to call, and calls the underlying RPC.
          Normally, this method receives a single argument (a struct or instance
          corresponding to the RPC request object). Defining this field will add
          one or more overloads providing flattened or simpler method signatures
          in some languages.

          The fields on the method signature are provided as a comma-separated
          string.

          For example, the proto RPC and annotation:

          rpc CreateSubscription(CreateSubscriptionRequest) returns (Subscription)
          { option (google.api.method_signature) = "name,topic"; }

          Would add the following Java overload (in addition to the method
          accepting the request object):

          public final Subscription createSubscription(String name, String topic)

          The following backwards-compatibility guidelines apply:

          -  Adding this annotation to an unannotated method is backwards
             compatible.
          -  Adding this annotation to a method which already has existing method
             signature annotations is backwards compatible if and only if the new
             method signature annotation is last in the sequence.
          -  Modifying or removing an existing method signature annotation is a
             breaking change.
          -  Re-ordering existing method signature annotations is a breaking
             change.
          DISTRIBUTION (int): ``Any`` contains an arbitrary serialized protocol buffer message
          along with a URL that describes the type of the serialized message.

          Protobuf library provides support to pack/unpack Any values in the form
          of utility functions or additional generated methods of the Any type.

          Example 1: Pack and unpack a message in C++.

          ::

              Foo foo = ...;
              Any any;
              any.PackFrom(foo);
              ...
              if (any.UnpackTo(&foo)) {
                ...
              }

          Example 2: Pack and unpack a message in Java.

          ::

              Foo foo = ...;
              Any any = Any.pack(foo);
              ...
              if (any.is(Foo.class)) {
                foo = any.unpack(Foo.class);
              }

          Example 3: Pack and unpack a message in Python.

          ::

              foo = Foo(...)
              any = Any()
              any.Pack(foo)
              ...
              if any.Is(Foo.DESCRIPTOR):
                any.Unpack(foo)
                ...

          Example 4: Pack and unpack a message in Go

          ::

               foo := &pb.Foo{...}
               any, err := ptypes.MarshalAny(foo)
               ...
               foo := &pb.Foo{}
               if err := ptypes.UnmarshalAny(any, foo); err != nil {
                 ...
               }

          The pack methods provided by protobuf library will by default use
          'type.googleapis.com/full.type.name' as the type URL and the unpack
          methods only use the fully qualified type name after the last '/' in the
          type URL, for example "foo.bar.com/x/y.z" will yield type name "y.z".

          # JSON

          The JSON representation of an ``Any`` value uses the regular
          representation of the deserialized, embedded message, with an additional
          field ``@type`` which contains the type URL. Example:

          ::

              package google.profile;
              message Person {
                string first_name = 1;
                string last_name = 2;
              }

              {
                "@type": "type.googleapis.com/google.profile.Person",
                "firstName": <string>,
                "lastName": <string>
              }

          If the embedded message type is well-known and has a custom JSON
          representation, that representation will be embedded adding a field
          ``value`` which holds the custom JSON in addition to the ``@type``
          field. Example (for message ``google.protobuf.Duration``):

          ::

              {
                "@type": "type.googleapis.com/google.protobuf.Duration",
                "value": "1.212s"
              }
          MONEY (int): The value is money.
        """

        VALUE_TYPE_UNSPECIFIED = 0
        BOOL = 1
        INT64 = 2
        DOUBLE = 3
        STRING = 4
        DISTRIBUTION = 5
        MONEY = 6
