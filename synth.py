# Copyright 2018 Google LLC
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

"""This script is used to synthesize generated parts of this library."""
import synthtool as s
from synthtool import gcp
from synthtool.languages import python

gapic = gcp.GAPICBazel()
common = gcp.CommonTemplates()

# ----------------------------------------------------------------------------
# Generate logging GAPIC layer
# ----------------------------------------------------------------------------
library = gapic.py_library(
    service="logging",
    version="v2",
    bazel_target="//google/logging/v2:logging-v2-py",
    include_protos=True,
)

# the structure of the logging directory is a bit different, so manually copy the protos
s.move(library / "google/cloud/logging_v2/proto", "google/cloud/logging_v2/proto")

s.move(library / "google/cloud/logging_v2/gapic")
s.move(library / "tests/unit/gapic/v2")
# Don't include gapic library docs. Users should use the hand-written layer instead
# s.move(library / "docs/gapic/v2")

# ----------------------------------------------------------------------------
# Add templated files
# ----------------------------------------------------------------------------
templated_files = common.py_library(
    unit_cov_level=95,
    cov_level=99,
    system_test_python_versions = ['3.8'],
    unit_test_python_versions = ['3.5', '3.6', '3.7', '3.8'],
    system_test_external_dependencies = [
        'google-cloud-bigquery',
        'google-cloud-pubsub',
        'google-cloud-storage',
        'google-cloud-testutils'
    ],
    unit_test_external_dependencies = [
       'flask',
       'webob',
       'django'
    ],
    samples=True,
)
s.move(templated_files, excludes=[".coveragerc"])

# --------------------------------------------------------------------------
# Samples templates
# --------------------------------------------------------------------------

python.py_samples()

s.shell.run(["nox", "-s", "blacken"], hide_output=False)