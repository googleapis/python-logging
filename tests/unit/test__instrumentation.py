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

import unittest
import google.cloud.logging_v2._instrumentation as i


class TestInstrumentation(unittest.TestCase):

    TEST_NAME = "python"
    # LONG_NAME > 14 characters
    LONG_NAME = TEST_NAME + "789ABCDEF"

    TEST_VERSION = "1.0.0"
    # LONG_VERSION > 16 characters
    LONG_VERSION = TEST_VERSION + "6789ABCDEF12"

    def _get_diagonstic_value(self, entry, key):
        return entry.payload[i._DIAGNOSTIC_INFO_KEY][i._INSTRUMENTATION_SOURCE_KEY][-1][
            key
        ]

    def test_default_diagnostic_info(self):
        entry = i._create_diagnostic_entry()
        self.assertEqual(
            i._PYTHON_LIBRARY_NAME,
            self._get_diagonstic_value(entry, "name"),
        )
        self.assertEqual(
            i._LIBRARY_VERSION, self._get_diagonstic_value(entry, "version")
        )

    def test_custom_diagnostic_info(self):
        entry = i._create_diagnostic_entry(
            name=self.TEST_NAME, version=self.TEST_VERSION
        )
        self.assertEqual(
            self.TEST_NAME,
            self._get_diagonstic_value(entry, "name"),
        )
        self.assertEqual(
            self.TEST_VERSION, self._get_diagonstic_value(entry, "version")
        )

    def test_truncate_long_values(self):
        entry = i._create_diagnostic_entry(
            name=self.LONG_NAME, version=self.LONG_VERSION
        )

        expected_name = self.LONG_NAME[: i._MAX_NAME_LENGTH] + "*"
        expected_version = self.LONG_VERSION[: i._MAX_VERSION_LENGTH] + "*"

        self.assertEqual(expected_name, self._get_diagonstic_value(entry, "name"))
        self.assertEqual(expected_version, self._get_diagonstic_value(entry, "version"))

    def test_validate_and_update_instrumentation_adds_info(self):
        info = i._validate_and_update_instrumentation()
        self.assertEqual(1, len(info))
        self.assertEqual(i._PYTHON_LIBRARY_NAME, info[-1]["name"])
        self.assertEqual(i._LIBRARY_VERSION, info[-1]["version"])

    def test_validate_and_update_instrumentation_corrects_existing(self):
        existing_info = [
            {"name": self.TEST_NAME, "version": "0.0.0"},
            {"name": self.LONG_NAME, "version": self.LONG_VERSION},
        ]

        info = i._validate_and_update_instrumentation(existing_info)

        self.assertEqual(3, len(info))
        self.assertEqual("0.0.0", info[0]["version"])
        self.assertEqual(self.TEST_NAME, info[0]["name"])
        expected_version = self.LONG_VERSION[: i._MAX_VERSION_LENGTH] + "*"
        self.assertEqual(expected_version, info[1]["version"])
        expected_name = self.LONG_NAME[: i._MAX_NAME_LENGTH] + "*"
        self.assertEqual(expected_name, info[1]["name"])
        self.assertEqual(i._LIBRARY_VERSION, info[2]["version"])
        self.assertEqual(i._PYTHON_LIBRARY_NAME, info[2]["name"])

    def test_validate_and_update_instrumentation_truncates_entries(self):
        existing_info = [
            {"name": self.TEST_NAME, "version": "0.0.1"},
            {"name": self.TEST_NAME, "version": "0.0.2"},
            {"name": self.TEST_NAME, "version": "0.0.3"},
            {"name": self.TEST_NAME, "version": "0.0.4"},
        ]
        info = i._validate_and_update_instrumentation(existing_info)

        self.assertEqual(3, len(info))
        self.assertEqual(i._LIBRARY_VERSION, info[2]["version"])
        self.assertEqual(i._PYTHON_LIBRARY_NAME, info[2]["name"])

    def test_is_valid(self):
        invalid_name = {"name": "foo-logging", "version": "3.0.0"}
        no_name = {"version": "3.0.0"}

        valid = {"name": i._PYTHON_LIBRARY_NAME, "version": i._LIBRARY_VERSION}

        self.assertFalse(i._is_valid(invalid_name))
        self.assertFalse(i._is_valid(no_name))

        self.assertTrue(i._is_valid(valid))
