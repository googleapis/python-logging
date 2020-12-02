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



class TestCommon(object):
    _client = Client()

    def _run_command(self, command, args=None):
        script_dir = os.path.dirname(os.path.realpath(__file__))
        os.chdir(script_dir)
        os.setpgrp()
        complete = False
        try:
            full_command = [f'./test-code/{self.environment_name()}.sh'] + split(command)
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

    def _get_logs(self, timestamp=None):
        time_format = "%Y-%m-%dT%H:%M:%S.%f%z"
        if not timestamp:
            timestamp = datetime.now(timezone.utc) - timedelta(minutes=10)
        _, filter_str = self._run_command('filter-string')
        filter_str += ' AND timestamp > "%s"' % timestamp.strftime(time_format)
        iterator = self._client.list_entries(filter_=filter_str)
        entries = list(iterator)
        return entries

    def trigger(self, function):
        self._run_command('trigger', function)
        # give the command time to be received
        sleep(30)

    def setUp(self):
        # deploy test code to GCE
        status, _ = self._run_command('deploy')
        self.assertTrue(status)
        # verify code is running
        status, _ = self._run_command('verify')
        self.assertEqual(status, 0)

    def tearDown(self):
        # by default, destroy environment on each run
        # allow skipping deletion for development
        if not os.getenv("NO_CLEAN"):
            self._run_command('destroy')

    def test_receive_log(self):
        timestamp = datetime.now(timezone.utc)
        self.trigger('test_1')
        log_list = self._get_logs(timestamp)
        self.assertTrue(log_list)
        self.assertEqual(len(log_list), 1)
        log = log_list[0]
        self.assertTrue(isinstance(log, entries.StructEntry))
        self.assertEqual(log.payload['message'], 'test_1')
        self.assertEqual(log.severity, LogSeverity.WARNING)

