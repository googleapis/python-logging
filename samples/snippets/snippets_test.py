# Copyright 2016 Google Inc. All Rights Reserved.
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

import uuid

import backoff
from google.api_core.exceptions import NotFound
from google.cloud import logging
import pytest

import snippets


TEST_LOGGER_NAME = "example_log_{}".format(uuid.uuid4().hex)


@pytest.fixture
def example_log():
    client = logging.Client()
    logger = client.logger(TEST_LOGGER_NAME)
    text = "Hello, world."
    logger.log_text(text)
    return text


def test_list(example_log, capsys):
    @backoff.on_exception(backoff.expo, AssertionError, max_time=120)
    def eventually_consistent_test():
        snippets.list_entries(TEST_LOGGER_NAME)
        out, _ = capsys.readouterr()
        assert example_log in out

    eventually_consistent_test()


def test_write():
    snippets.write_entry(TEST_LOGGER_NAME)


def test_delete(example_log, capsys):
    @backoff.on_exception(backoff.expo, NotFound, max_time=120)
    def eventually_consistent_test():
        snippets.delete_logger(TEST_LOGGER_NAME)
        out, _ = capsys.readouterr()
        assert TEST_LOGGER_NAME in out
