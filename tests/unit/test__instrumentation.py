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

class TestInstrumentation(unittest.TestCase):

    def test_default_diagnostic_info(self):
        import google.cloud.logging_v2._instrumentation as i

        entry = i.create_diagnostic_entry()
        self.assertEqual(entry.payload[i._DIAGNOSTIC_INFO_KEY][i._INSTRUMENTATION_SOURCE_KEY]["name"], i._PYTHON_LIBRARY_NAME)
        self.assertEqual(entry.payload[i._DIAGNOSTIC_INFO_KEY][i._INSTRUMENTATION_SOURCE_KEY]["version"], i._LIBRARY_VERSION)