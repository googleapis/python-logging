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
        self.script_path = os.path.join(run_dir, f'test_code/{environment}.sh')
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



