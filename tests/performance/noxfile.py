# -*- coding: utf-8 -*-
#
# Copyright 2022 Google LLC
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

# Generated by synthtool. DO NOT EDIT!

from __future__ import absolute_import
import os
import pathlib
import re
import shutil
import warnings

import nox


DEFAULT_PYTHON_VERSION = "3.8"

PERFORMANCE_TEST_PYTHON_VERSIONS = ["3.8"]

CURRENT_DIRECTORY = pathlib.Path(__file__).parent.absolute()
REPO_ROOT_DIRECTORY = CURRENT_DIRECTORY.parent.parent

# 'docfx' is excluded since it only needs to run in 'docs-presubmit'
nox.options.sessions = [
    "performance",
]

# Error if a python version is missing
nox.options.error_on_missing_interpreters = True

@nox.session(python=PERFORMANCE_TEST_PYTHON_VERSIONS)
def performance(session):
    """Run the performance test suite."""
    # Use pre-release gRPC for performance tests.
    session.install("--pre", "grpcio")

    # Install all test dependencies, then install this package into the
    # virtualenv's dist-packages.
    session.install(
        "mock",
        "pandas",
        "rich",
        "pytest",
        "google-cloud-testutils",
    )
    session.install("-e", str(REPO_ROOT_DIRECTORY))


    session.run(
        "py.test",
        "-s",
        f"--junitxml=perf_{session.python}_sponge_log.xml",
        str(CURRENT_DIRECTORY),
        *session.posargs,
    )
    # print quick summary of results from junitxml file
    print("junitxml results:")
    with open(f"perf_{session.python}_sponge_log.xml", "r") as file:
        data = file.read().replace('\n', '')
        total = 0
        for entry in data.split("testcase classname")[1:]:
            name = re.search('name="+(\w+)', entry)[1]
            time =  re.search('time="+([0-9\.]+)', entry)[1]
            total += float(time)
            print(f"\t{name}: {time}s")
        print(f"\tTotal: {total:.3f}s")

