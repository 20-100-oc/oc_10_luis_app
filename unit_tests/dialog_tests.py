# To run the test from terminal: python -m unittest <path to this file>
# exemple: python -m unittest unit_tests/dialog_tests.py

import os
import unittest

from azure.cognitiveservices.language.luis.runtime import LUISRuntimeClient
from msrest.authentication import CognitiveServicesCredentials



class TestConfig:
    PORT = int(os.environ.get("PORT", ""))
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    LUIS_APP_ID = os.environ.get("LuisAppId", "")
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "")
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "")
    APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get("AppInsightsInstrumentationKey", "")
    LUIS_APP_ENDPOINT = os.environ.get("LuisAppEndpoint", "")



class BookingFlightTest(unittest.TestCase):

    def setUp(self):
        config = TestConfig()
        luis_app_id = config.LUIS_APP_ID
        luis_api_key = config.LUIS_API_KEY
        luis_app_endpoint = config.LUIS_APP_ENDPOINT

        runtimeCredentials = CognitiveServicesCredentials(luis_api_key)
        runtime_client = LUISRuntimeClient(endpoint=luis_app_endpoint, credentials=runtimeCredentials)

        self.luis_app_id = luis_app_id
        self.runtime_client = runtime_client


    def extract_entity(self, entity_name, response):
        entity = None
        for entity_dict in response.entities:
            if entity_dict.type == entity_name:
                entity = entity_dict.entity
        return entity


    def test_intent(self):
        request = 'Book a flight from paris to london on february 10 2023. I will return on february 17 2023.'
        expected_intent = 'BookFlight'

        response = self.runtime_client.prediction.resolve(self.luis_app_id, query=request)
        received_intent = response.top_scoring_intent.intent

        self.assertEqual(received_intent, expected_intent)
        return received_intent


    def test_cities(self):
        request = 'Could you plan a trip from london to paris for me ?'
        expected_origin_city = 'london'
        expected_destination_city = 'paris'
        
        response = self.runtime_client.prediction.resolve(self.luis_app_id, query=request)
        received_origin_city = self.extract_entity('or_city', response)
        received_destination_city = self.extract_entity('dst_city', response)
        
        self.assertEqual(received_origin_city, expected_origin_city)
        self.assertEqual(received_destination_city, expected_destination_city)
        return received_origin_city, received_destination_city


    def test_dates(self):
        request = 'I want to book a flight on december 21 and return on december 30 for my birthday.'
        expected_start_date = 'december 21'
        expected_end_date = 'december 30'
        
        response = self.runtime_client.prediction.resolve(self.luis_app_id, query=request)
        received_start_date = self.extract_entity('str_date', response)
        received_end_date = self.extract_entity('end_date', response)

        self.assertEqual(received_start_date, expected_start_date)
        self.assertEqual(received_end_date, expected_end_date)
        return received_start_date, received_end_date


    def test_budget(self):
        request = 'I only have 200 dollars to spare, is there a flight to berlin for that ?'
        expected_budget = '200'
        
        response = self.runtime_client.prediction.resolve(self.luis_app_id, query=request)
        received_budget = self.extract_entity('budget', response)
        
        self.assertEqual(received_budget, expected_budget)
        return received_budget



if __name__ == '__main__':
    unittest.main()
