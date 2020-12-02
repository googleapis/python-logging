import google.cloud.logging
from google.cloud._helpers import UTC
from google.cloud.logging_v2.handlers.handlers import CloudLoggingHandler
from google.cloud.logging_v2.handlers.transports import SyncTransport
from google.cloud.logging_v2 import Client
from google.cloud.logging_v2.resource import Resource
from google.cloud.logging_v2 import entries
from google.cloud.logging_v2._helpers import LogSeverity

from time import sleep
from datetime import datetime
from datetime import timezone
import os
import sys
from shlex import split
import subprocess
import signal
from enum import Enum

class Command(Enum):
    Deploy = "deploy"
    Destroy = "destroy"
    Verify = "verify"
    GetFilter = "filter-string"
    Trigger = "trigger"

class ScriptInterface:

    def __init__(self, environment):
        run_dir = os.path.dirname(os.path.realpath(__file__))
        self.script_path = os.path.join(run_dir, f'test-code/{environment}.sh')
        print(self.script_path)
        if not os.path.exists(self.script_path):
            raise RuntimeError(f'environment {environment} does not exist')

    def run_command(self, command, args=None):
        if not command or not isinstance(command, Command):
            raise RuntimeError(f'unknown command: {command}')
        os.setpgrp()
        complete = False
        try:
            full_command = [self.script_path] + split(command.value)
            print(full_command)
            if args:
                full_command += split(args)
            result = subprocess.run(full_command, capture_output=True)
            complete=True
            return result.returncode, result.stdout.decode('utf-8')
        except Exception as e:
            print(e)
        finally:
            if not complete:
                # kill background process if script is terminated
                # os.killpg(0, signal.SIGTERM)
                return 1, None


class TestGCPCommon:
    _client = Client()
    # environment name must be set by subclass
    environment = None

    def _get_logs(self, timestamp=None):
        time_format = "%Y-%m-%dT%H:%M:%S.%f%z"
        if not timestamp:
            timestamp = datetime.now(timezone.utc) - timedelta(minutes=10)
        _, filter_str = self._script.run_command(Command.GetFilter)
        filter_str += ' AND timestamp > "%s"' % timestamp.strftime(time_format)
        iterator = self._client.list_entries(filter_=filter_str)
        entries = list(iterator)
        return entries

    def _trigger(self, function, return_logs=True):
        timestamp = datetime.now(timezone.utc)
        self._script.run_command(Command.Trigger, function)
        # give the command time to be received
        sleep(30)
        if return_logs:
            log_list = self._get_logs(timestamp)
            return log_list

    @classmethod
    def setUpClass(cls):
        if not cls.environment:
            raise NotImplementedError('environment not set by subclass')
        cls._script = ScriptInterface(cls.environment)
        # check if already setup
        status, _ = cls._script.run_command(Command.Verify)
        if status == 0:
            if os.getenv("NO_CLEAN"):
                # ready to go
                return
            else:
                # reset environment
                status, _ = cls._script.run_command(Command.Destroy)
                assert status == 0
        # deploy test code to GCE
        status, _ = cls._script.run_command(Command.Deploy)
        # verify code is running
        status, _ = cls._script.run_command(Command.Verify)
        assert status == 0

    @classmethod
    def tearDown_class(cls):
        # by default, destroy environment on each run
        # allow skipping deletion for development
        if not os.getenv("NO_CLEAN"):
            cls._script.run_command(Command.Destroy)

    def test_receive_log(self):
        log_list = self._trigger('test_1')
        self.assertTrue(log_list)
        self.assertEqual(len(log_list), 1)
        log = log_list[0]
        self.assertTrue(isinstance(log, entries.StructEntry))
        self.assertEqual(log.payload['message'], 'test_1')
        self.assertEqual(log.severity, LogSeverity.WARNING)

