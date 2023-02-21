#TODO add new entities

# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from enum import Enum
from typing import Dict
from botbuilder.ai.luis import LuisRecognizer
from botbuilder.core import IntentScore, TopIntent, TurnContext

from booking_details import BookingDetails


class Intent(Enum):
    BOOK_FLIGHT = "BookFlight"
    #CANCEL = "Cancel"
    #GET_WEATHER = "GetWeather"
    #NONE_INTENT = "NoneIntent"
    NONE_INTENT = "None"

def top_intent(intents: Dict[Intent, dict]) -> TopIntent:
    max_intent = Intent.NONE_INTENT
    max_value = 0.0

    for intent, value in intents:
        intent_score = IntentScore(value)
        if intent_score.score > max_value:
            max_intent, max_value = intent, intent_score.score

    return TopIntent(max_intent, max_value)


class LuisHelper:
    @staticmethod
    async def execute_luis_query(luis_recognizer: LuisRecognizer, turn_context: TurnContext) -> (Intent, object):
        """
        Returns an object with preformatted LUIS results for the bot's dialogs to consume.
        """
        result = None
        intent = None

        try:
            recognizer_result = await luis_recognizer.recognize(turn_context)

            intent = (
                sorted(
                    recognizer_result.intents,
                    key=recognizer_result.intents.get,
                    reverse=True,
                )[:1][0]
                if recognizer_result.intents
                else None
            )

            if intent == Intent.BOOK_FLIGHT.value:
                result = BookingDetails()

                '''
                # We need to get the result from the LUIS JSON which at every level returns an array.
                to_entities = recognizer_result.entities.get("$instance", {}).get("To", [])
                if len(to_entities) > 0:
                    if recognizer_result.entities.get("To", [{"$instance": {}}])[0][
                        "$instance"
                    ]:
                        result.destination = to_entities[0]["text"].capitalize()
                    else:
                        result.unsupported_airports.append(
                            to_entities[0]["text"].capitalize()
                        )

                from_entities = recognizer_result.entities.get("$instance", {}).get("From", [])
                if len(from_entities) > 0:
                    if recognizer_result.entities.get("From", [{"$instance": {}}])[0][
                        "$instance"
                    ]:
                        result.origin = from_entities[0]["text"].capitalize()
                    else:
                        result.unsupported_airports.append(
                            from_entities[0]["text"].capitalize()
                        )

                # This value will be a TIMEX. And we are only interested in a Date so grab the first result and drop
                # the Time part. TIMEX is a format that represents DateTime expressions that include some ambiguity.
                # e.g. missing a Year.
                date_entities = recognizer_result.entities.get("datetime", [])
                if date_entities:
                    timex = date_entities[0]["timex"]

                    if timex:
                        datetime = timex[0].split("T")[0]

                        result.travel_date = datetime

                else:
                    result.travel_date = None
                '''


                # "or_city" entity
                or_city = recognizer_result.entities.get('or_city', [])
                #print('or_city:', or_city)
                if len(or_city) > 0:
                    result.or_city = or_city[0].capitalize()

                # "dst_city" entity
                dst_city = recognizer_result.entities.get('dst_city', [])
                #print('dst_city:', dst_city)
                if len(dst_city) > 0:
                    result.dst_city = dst_city[0].capitalize()
                
                # "str_date" entity
                str_date = recognizer_result.entities.get('str_date', [])
                #print('str_date:', str_date)
                if len(str_date) > 0:
                    '''
                    timex = str_date[0]["timex"]
                    if timex:
                        datetime = timex[0].split("T")[0]
                        result.str_date = datetime
                    '''
                    result.str_date = str_date[0]
                
                # "end_date" entity
                end_date = recognizer_result.entities.get('end_date', [])
                #print('end_date:', end_date)
                if len(end_date) > 0:
                    '''
                    timex = end_date[0]["timex"]
                    if timex:
                        datetime = timex[0].split("T")[0]
                        result.end_date = datetime
                    '''
                    result.end_date = end_date[0]
                
                # "budget" entity
                budget = recognizer_result.entities.get('budget', [])
                #print('budget:', budget)
                if len(budget) > 0:
                    result.budget = budget[0]


        except Exception as exception:
            print('\nEncountered exeption in "luis_helper.py":')
            print(exception, '\n')

        return intent, result
