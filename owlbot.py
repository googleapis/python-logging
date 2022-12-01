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

for library in s.get_staging_dirs(default_version):
    if clean_up_generated_samples:
        shutil.rmtree("samples/generated_samples", ignore_errors=True)
        clean_up_generated_samples = False

    s.move([library], excludes=[
            "**/gapic_version.py",
            "setup.py",
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
    ],
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

s.shell.run(["nox", "-s", "blacken"], hide_output=False)
s.shell.run(["nox", "-s", "blacken"], cwd="samples/snippets", hide_output=False)

# --------------------------------------------------------------------------
# Modify test configs
# --------------------------------------------------------------------------

# add shared environment variables to test configs
tracked_subdirs = ["continuous", "presubmit", "release", "samples", "docs"]
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
