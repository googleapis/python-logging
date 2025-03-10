# Copyright 2022 Google LLC
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

import glob
import json
import os
import shutil

import synthtool as s
import synthtool.gcp as gcp
from synthtool.languages import python

# ----------------------------------------------------------------------------
# Copy the generated client from the owl-bot staging directory
# ----------------------------------------------------------------------------

clean_up_generated_samples = True

# Load the default version defined in .repo-metadata.json.
default_version = json.load(open(".repo-metadata.json", "rt")).get("default_version")

def place_before(path, text, *before_text, escape=None):
    replacement = "\n".join(before_text) + "\n" + text
    if escape:
        for c in escape:
            text = text.replace(c, '\\' + c)
    s.replace([path], text, replacement)

test_metrics_default_client_info_headers = \
"""def test_metrics_default_client_info_headers():
    import re

    # test that DEFAULT_CLIENT_INFO contains the expected gapic headers
    gapic_header_regex = re.compile(
        r"gapic\\\\/[0-9]+\\.[\\\\w.-]+ gax\\/[0-9]+\.[\\\\w.-]+ gl-python\\/[0-9]+\\.[\\\\w.-]+ grpc\\/[0-9]+\.[\\\\w.-]+"
    )
    detected_info = (
        google.cloud.logging_v2.services.metrics_service_v2.transports.base.DEFAULT_CLIENT_INFO
    )
    assert detected_info is not None
    detected_agent = " ".join(sorted(detected_info.to_user_agent().split(" ")))
    assert gapic_header_regex.match(detected_agent)\n\n\n"""

for library in s.get_staging_dirs(default_version):
    if clean_up_generated_samples:
        shutil.rmtree("samples/generated_samples", ignore_errors=True)
        clean_up_generated_samples = False

    place_before(
        library / "tests/unit/gapic/logging_v2/test_metrics_service_v2.py",
        "def test_metrics_service_v2_client_get_transport_class()",
        test_metrics_default_client_info_headers,
        escape="()",
    )

    s.move([library], excludes=[
            "**/gapic_version.py",
            "setup.py",
            "testing/constraints*.txt",
            "README.rst",
            "google/cloud/logging/__init__.py",  # generated types are hidden from users
            "google/cloud/logging_v2/__init__.py",
            "docs/index.rst",
            "docs/logging_v2",  # Don't include gapic library docs. Users should use the hand-written layer instead
            "scripts/fixup_logging_v2_keywords.py",  # don't include script since it only works for generated layer
        ],
    )

s.remove_staging_dirs()

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------

templated_files = gcp.CommonTemplates().py_library(
    cov_level=99,
    microgenerator=True,
    versions=gcp.common.detect_versions(path="./google", default_first=True),
    system_test_external_dependencies=[
        "google-cloud-bigquery",
        "google-cloud-pubsub",
        "google-cloud-storage",
        "google-cloud-testutils",
        "opentelemetry-sdk"
    ],
    system_test_python_versions=["3.12"],
    unit_test_external_dependencies=["flask", "webob", "django"],
    samples=True,
)

s.move(templated_files, 
    excludes=[
        "docs/index.rst",
        ".github/release-please.yml",
        ".coveragerc",
        "docs/multiprocessing.rst",
        ".github/workflows", # exclude gh actions as credentials are needed for tests
        ".github/auto-label.yaml",
        "README.rst", # This repo has a customized README
    ],
)
s.replace("noxfile.py",
"""prerel_deps = \[
        "protobuf",""",
"""prerel_deps = [
        "google-cloud-audit-log",
        "protobuf",""",
)

# adjust .trampolinerc for environment tests
s.replace(".trampolinerc", "required_envvars[^\)]*\)", "required_envvars+=()")
s.replace(
    ".trampolinerc",
    "pass_down_envvars\+\=\(",
    'pass_down_envvars+=(\n    "ENVIRONMENT"\n    "RUNTIME"',
)

# don't lint environment tests
s.replace(
    ".flake8",
    "exclude =",
    "exclude =\n  # Exclude environment test code.\n  tests/environment/**\n",
)

# use conventional commits for renovate bot
s.replace(
    "renovate.json",
    """}
}""",
    """},
  "semanticCommits": "enabled"
}""",
)

# --------------------------------------------------------------------------
# Samples templates
# --------------------------------------------------------------------------

python.py_samples()

# For autogenerated sample code, resolve object paths by finding the specific subpackage
# the object belongs to. This is because we leave out all autogenerated packages from the
# __init__.py of logging_v2. For now, this is manually copy-pasted from the __all__s of each
# subpackage's __init__.py.
gapic_objects =  {
    "logging_v2.services.config_service_v2": [
        "ConfigServiceV2Client",
        "ConfigServiceV2AsyncClient"
    ],
    "logging_v2.services.logging_service_v2": [
        "LoggingServiceV2Client",
        "LoggingServiceV2AsyncClient"
    ],
    "logging_v2.services.metrics_service_v2": [
        "MetricsServiceV2Client",
        "MetricsServiceV2AsyncClient"
    ],
    "logging_v2.types": [
        "LogEntry",
        "LogEntryOperation",
        "LogEntrySourceLocation",
        "LogSplit",
        "DeleteLogRequest",
        "ListLogEntriesRequest",
        "ListLogEntriesResponse",
        "ListLogsRequest",
        "ListLogsResponse",
        "ListMonitoredResourceDescriptorsRequest",
        "ListMonitoredResourceDescriptorsResponse",
        "TailLogEntriesRequest",
        "TailLogEntriesResponse",
        "WriteLogEntriesPartialErrors",
        "WriteLogEntriesRequest",
        "WriteLogEntriesResponse",
        "BigQueryDataset",
        "BigQueryOptions",
        "BucketMetadata",
        "CmekSettings",
        "CopyLogEntriesMetadata",
        "CopyLogEntriesRequest",
        "CopyLogEntriesResponse",
        "CreateBucketRequest",
        "CreateExclusionRequest",
        "CreateLinkRequest",
        "CreateSinkRequest",
        "CreateViewRequest",
        "DeleteBucketRequest",
        "DeleteExclusionRequest",
        "DeleteLinkRequest",
        "DeleteSinkRequest",
        "DeleteViewRequest",
        "GetBucketRequest",
        "GetCmekSettingsRequest",
        "GetExclusionRequest",
        "GetLinkRequest",
        "GetSettingsRequest",
        "GetSinkRequest",
        "GetViewRequest",
        "IndexConfig",
        "Link",
        "LinkMetadata",
        "ListBucketsRequest",
        "ListBucketsResponse",
        "ListExclusionsRequest",
        "ListExclusionsResponse",
        "ListLinksRequest",
        "ListLinksResponse",
        "ListSinksRequest",
        "ListSinksResponse",
        "ListViewsRequest",
        "ListViewsResponse",
        "LocationMetadata",
        "LogBucket",
        "LogExclusion",
        "LogSink",
        "LogView",
        "Settings",
        "UndeleteBucketRequest",
        "UpdateBucketRequest",
        "UpdateCmekSettingsRequest",
        "UpdateExclusionRequest",
        "UpdateSettingsRequest",
        "UpdateSinkRequest",
        "UpdateViewRequest",
        "IndexType",
        "LifecycleState",
        "OperationState",
        "CreateLogMetricRequest",
        "DeleteLogMetricRequest",
        "GetLogMetricRequest",
        "ListLogMetricsRequest",
        "ListLogMetricsResponse",
        "LogMetric",
        "UpdateLogMetricRequest"
    ]
}

sample_files = glob.glob("samples/generated_samples/logging_v2_*.py")
for subpackage_name in gapic_objects:
    for object_name in gapic_objects[subpackage_name]:
        text = "logging_v2." + object_name
        replacement = subpackage_name + "." + object_name
        s.replace(sample_files, text, replacement)

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
s.shell.run(["nox", "-s", "blacken"], cwd="samples/snippets", hide_output=False)

# --------------------------------------------------------------------------
# Modify test configs
# --------------------------------------------------------------------------

# add shared environment variables to test configs
tracked_subdirs = ["continuous", "presubmit", "samples"]
for subdir in tracked_subdirs:
    for path, subdirs, files in os.walk(f".kokoro/{subdir}"):
        for name in files:
            if name == "common.cfg":
                file_path = os.path.join(path, name)
                s.move(
                    ".kokoro/common_env_vars.cfg",
                    file_path,
                    merge=lambda src, dst, _,: f"{dst}\n{src}",
                )
