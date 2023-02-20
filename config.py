#!/usr/bin/env python
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Configuration for the bot."""

import os



class DefaultConfig:
    """Configuration for the bot."""

    '''
    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    LUIS_APP_ID = os.environ.get("LuisAppId", "448b542a-1140-48af-a909-207052d7fc5a")
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "ec52dd6d1e7449b1b0e33adead613bb4")
    # LUIS endpoint host name, ie "<region>.api.cognitive.microsoft.com"
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "westeurope.api.cognitive.microsoft.com")
    APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get(
        "AppInsightsInstrumentationKey", "5d20c1e7-4c90-44aa-89e6-ed28c9d458eb"
    )
    '''
    """
    try:
        # local execution
        from .local_config_file import get_env_variables
        secrets = get_env_variables
        for key_name in secrets:
            print(key_name)
            key = secrets[key_name]
            print(key, '\n')
            os.environ[key_name] = key
    except:
        # execution on azure web app
        pass
    """
    PORT = int(os.environ.get("PORT", ""))
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    LUIS_APP_ID = os.environ.get("LuisAppId", "")
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "")
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "")
    APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get("AppInsightsInstrumentationKey", "")
