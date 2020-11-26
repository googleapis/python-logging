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

from datetime import datetime, timedelta, timezone
import logging
import unittest
import os
import subprocess
from shlex import split
import sys
import signal

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

from time import sleep

def _run_command(command):
    os.chdir(os.path.abspath(sys.path[0]))
    os.setpgrp()
    complete = False
    try:
        result = subprocess.run(split(command), capture_output=True)
        complete=True
        return result.returncode, result.stdout.decode('utf-8')
    except Exception as e:
        print(e)
    finally:
        # kill background process if script is terminated
        if not complete:
            os.killpg(0, signal.SIGTERM)

def deploy():
    """Deploy test code to GCE"""
    if verify():
        if os.getenv("NO_CLEAN"):
            # allow a way for us to skip expensive recreation on each run
            return True
        else:
            # if instance already exists, destroy and recreate it
            destroy()
    create_command = "./test-code/compute.sh deploy"
    statuscode, _ = _run_command(create_command)
    return statuscode == 0


def verify():
    """Verify test code is running on GCE"""
    verify_command = "./test-code/compute.sh verify"
    statuscode, _ = _run_command(verify_command)
    return statuscode == 0

def destroy():
    destroy_command = "./test-code/compute.sh destroy"
    _run_command(destroy_command)

def _get_resource_filter():
    filter_command = "./test-code/compute.sh filter-string"
    _, output = _run_command(filter_command)
    return output.replace("\n", "")

def trigger(function_name):
    trigger_command = f"./test-code/compute.sh trigger {function_name}"
    _run_command(trigger_command)
    # give the command time to be received
    sleep(10)

class TestGCE(unittest.TestCase):

    _client = Client()

    def _get_logs(self, timestamp=None):
        time_format = "%Y-%m-%dT%H:%M:%S.%f%z"
        if not timestamp:
            timestamp = datetime.now(timezone.utc) - timedelta(minutes=10)
        filter_str = _get_resource_filter()
        filter_str += ' AND timestamp > "%s"' % timestamp.strftime(time_format)
        iterator = self._client.list_entries(filter_=filter_str)
        entries = list(iterator)
        return entries

    def setUp(self):
        # deploy test code to GCE
        status = deploy()
        self.assertTrue(status)
        # verify code is running
        status = verify()
        self.assertTrue(status)

    def tearDown(self):
        # by default, destroy environment on each run
        # allow skipping deletion for development
        if not os.getenv("NO_CLEAN"):
            destroy()

    def test_test(self):
        timestamp = datetime.now(timezone.utc)
        trigger('test_1')
        logs = self._get_logs(timestamp)
        self.assertTrue(logs)


if __name__ == "__main__":
    cls = TestGCE()
    entries = cls._get_logs()
    print([e.payload['message'] for e in entries])
    sys.exit(1)
