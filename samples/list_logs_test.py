# Copyright 2025 Google LLC
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

import os
import list_logs
def test_list_logs(capsys):
    
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    
    list_logs.list_logs(project_id)

    out, _ = capsys.readouterr()
    assert "Logs:" in out