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
from google.cloud.logging_v2 import Client
from google.cloud.logging_v2.resource import Resource

from test_utils.retry import RetryErrors
from test_utils.retry import RetryResult
from test_utils.system import unique_resource_id


class TestGCE(unittest.TestCase):

    def _run_command(self, command):
        os.chdir(os.path.abspath(sys.path[0]))
        os.setpgrp()
        complete = False
        try:
            # run deploy.sh in a background shell
            process = subprocess.Popen(split(command))
            process.communicate()
            complete = True
            return process.returncode
        finally:
            # kill background process if script is terminated
            if not complete:
                os.killpg(0, signal.SIGTERM)


    def deploy(self):
        """Deploy test code to GCE"""
        if self.verify():
            # if instance already exists, recreate it
            # self.destroy()
            return True
        create_command = "./test-code/compute.sh deploy"
        statuscode = self._run_command(create_command)
        return statuscode == 0


    def verify(self):
        """Verify test code is running on GCE"""
        verify_command = "./test-code/compute.sh verify"
        statuscode = self._run_command(verify_command)
        return statuscode == 0

    def destroy(self):
        destroy_command = "./test-code/compute.sh destroy"
        self._run_command(destroy_command)

    def get_logs(self):
        pass

    def setUp(self):
        # deploy test code to GCE
        status = self.deploy()
        self.assertTrue(status)
        # verify code is running
        status = self.verify()
        self.assertTrue(status)

    def tearDown(self):
        #self.destroy()
        pass


    def test_test(self):
        self.assertTrue(True)

if __name__ == "__main__":
    sys.exit(1)
