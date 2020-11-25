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

import datetime
import logging
import unittest
import os
import subprocess
from shlex import split
import sys

from google.api_core.exceptions import BadGateway
from google.api_core.exceptions import Conflict
from google.api_core.exceptions import NotFound
from google.api_core.exceptions import TooManyRequests
from google.api_core.exceptions import ResourceExhausted
from google.api_core.exceptions import RetryError
from google.api_core.exceptions import ServiceUnavailable
import google.cloud.logging
from google.cloud._helpers import UTC
from google.cloud.logging_v2.handlers.handlers import CloudLoggingHandler
from google.cloud.logging_v2.handlers.transports import SyncTransport
from google.cloud.logging_v2 import client
from google.cloud.logging_v2.resource import Resource

from test_utils.retry import RetryErrors
from test_utils.retry import RetryResult
from test_utils.system import unique_resource_id


class TestGCE(unittest.TestCase):

    def deploy(self):
        """Deploy test code to GCE"""
        os.chdir(os.path.abspath(sys.path[0]))
        create_command = "./test-code/deploy.sh --environment gce"
        os.setpgrp()
        complete = False
        try:
            # run deploy.sh in a background shell
            process = subprocess.Popen(split(create_command), bufsize=0, shell=True)
            process.communicate()
            complete = True
        finally:
            # kill background process if script is terminated
            if not complete:
                os.killpg(0, signal.SIGTERM)

    def verify(self):
        """Verify test code is running on GCE"""
        os.chdir(os.path.abspath(sys.path[0]))
        create_command = "./test-code/verify.sh --environment gce"
        process = subprocess.Popen(split(create_command))
        process.communicate()
        self.assertEqual(process.returncode, 0)

    def setUp(self):
        self.deploy()
        self.verify()

    def tearDown(self):
        pass


    def test_test(self):
        self.assertTrue(True)
