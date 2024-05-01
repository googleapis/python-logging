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


# Utility functions to setup mock OpenTelemetry spans, needed by multiple test
# suites.

import contextlib
import mock

import opentelemetry.context
import opentelemetry.trace

from opentelemetry.trace.span import TraceFlags

_OTEL_SPAN_CONTEXT_TRACE_ID = 0x123456789123456789
_OTEL_SPAN_CONTEXT_SPAN_ID = 0x123456789
_OTEL_SPAN_CONTEXT_TRACEFLAGS = TraceFlags(TraceFlags.SAMPLED)

_EXPECTED_OTEL_TRACE_ID = "00000000000000123456789123456789"
_EXPECTED_OTEL_SPAN_ID = "0000000123456789"
_EXPECTED_OTEL_TRACESAMPLED = True


@contextlib.contextmanager
def _setup_otel_span_context():
    """Sets up a nonrecording OpenTelemetry span with a mock span context that gets returned
    by opentelemetry.trace.get_current_span, and returns it as a contextmanager
    """
    span_context = opentelemetry.trace.SpanContext(
        _OTEL_SPAN_CONTEXT_TRACE_ID,
        _OTEL_SPAN_CONTEXT_SPAN_ID,
        False,
        trace_flags=_OTEL_SPAN_CONTEXT_TRACEFLAGS,
    )
    span = opentelemetry.trace.NonRecordingSpan(span_context)
    with mock.patch("opentelemetry.trace.get_current_span", return_value=span) as m:
        yield m
