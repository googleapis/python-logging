# -*- coding: utf-8 -*-
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
#
# Generated code. DO NOT EDIT!
#
# Snippet for UpdateCmekSettings
# NOTE: This snippet has been automatically generated for illustrative purposes only.
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-cloud-logging


# [START logging_v2_generated_ConfigServiceV2_UpdateCmekSettings_async]
from google.cloud import logging_v2


async def sample_update_cmek_settings():
    # Create a client
    client = logging_v2.ConfigServiceV2AsyncClient()

    # Initialize request argument(s)
    request = logging_v2.UpdateCmekSettingsRequest(
        name="name_value",
    )

    # Make the request
    response = await client.update_cmek_settings(request=request)

    # Handle the response
    print(response)

# [END logging_v2_generated_ConfigServiceV2_UpdateCmekSettings_async]