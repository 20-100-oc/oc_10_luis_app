#TODO use confirm prompt ?
#TODO include new entities
#TODO rename original entities

# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Flight booking dialog."""

from datatypes_date_time.timex import Timex

from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory, BotTelemetryClient, NullTelemetryClient
from .cancel_and_help_dialog import CancelAndHelpDialog
from .date_resolver_dialog import DateResolverDialog
from .date_return_resolver_dialog import ReturnDateResolverDialog

import logging
from config import DefaultConfig
from opencensus.ext.azure.log_exporter import AzureLogHandler



class BookingDialog(CancelAndHelpDialog):
    """Flight booking implementation."""

    def __init__(
        self,
        dialog_id: str = None,
        telemetry_client: BotTelemetryClient = NullTelemetryClient(),
    ):
        super(BookingDialog, self).__init__(
            dialog_id or BookingDialog.__name__, telemetry_client
        )
        self.telemetry_client = telemetry_client
        text_prompt = TextPrompt(TextPrompt.__name__)
        text_prompt.telemetry_client = telemetry_client

        waterfall_dialog = WaterfallDialog(
            WaterfallDialog.__name__,
            [
                #self.destination_step,
                #self.origin_step,
                #self.travel_date_step,
                self.dst_city_step, 
                self.or_city_step, 
                self.str_date_step, 
                self.end_date_step, 
                self.budget_step, 
                self.confirm_step,  # was commented originaly
                self.final_step,
            ],
        )
        waterfall_dialog.telemetry_client = telemetry_client

        self.add_dialog(text_prompt)
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))  # was commented originaly
        self.add_dialog(
            DateResolverDialog(DateResolverDialog.__name__, self.telemetry_client)
        )
        self.add_dialog(
            ReturnDateResolverDialog(ReturnDateResolverDialog.__name__, self.telemetry_client)
        )
        self.add_dialog(waterfall_dialog)

        self.initial_dialog_id = WaterfallDialog.__name__


    async def dst_city_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for the destination city."""
        booking_details = step_context.options

        if booking_details.dst_city is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("To what city would you like to travel ?")
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.dst_city)


    async def or_city_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Prompt for the city of origin."""
        booking_details = step_context.options

        # Capture the response to the previous step's prompt
        booking_details.dst_city = step_context.result
        if booking_details.or_city is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("From what city will you be travelling ?")
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.or_city)


    async def str_date_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Prompt for travel date.
        This will use the DATE_RESOLVER_DIALOG."""

        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.or_city = step_context.result
        if booking_details.str_date is None or self.is_ambiguous(booking_details.str_date):
            return await step_context.begin_dialog(
                DateResolverDialog.__name__, booking_details.str_date
            )  # pylint: disable=line-too-long

        return await step_context.next(booking_details.str_date)
    

    async def end_date_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Prompt for return date.
        This will use the RETURN_DATE_RESOLVER_DIALOG."""

        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.str_date = step_context.result
        if booking_details.end_date is None or self.is_ambiguous(booking_details.end_date):
            return await step_context.begin_dialog(
                ReturnDateResolverDialog.__name__, booking_details.end_date
            )  # pylint: disable=line-too-long

        return await step_context.next(booking_details.end_date)


    async def budget_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Prompt for the trip's budget."""
        booking_details = step_context.options

        # Capture the response to the previous step's prompt
        booking_details.end_date = step_context.result
        if booking_details.budget is None:
            return await step_context.prompt(
                TextPrompt.__name__,
                PromptOptions(
                    prompt=MessageFactory.text("What is your budget for this trip ?")
                ),
            )  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.budget)


    async def confirm_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """Confirm the information the user has provided."""
        booking_details = step_context.options

        # Capture the results of the previous step
        booking_details.budget = step_context.result
        '''
        msg = (
            f"Please confirm, I have you traveling to: { booking_details.dst_city }"
            f" from: { booking_details.or_city } on: { booking_details.str_date}."
        )
        '''
        
        msg =f'''
        Please confirm, is this correct ?

            destination: {booking_details.dst_city}
                 origin: {booking_details.or_city}
         departure date: {booking_details.str_date}
            return date: {booking_details.end_date}
                 budget: {booking_details.budget}
        '''
        
        # Offer a YES/NO prompt.
        return await step_context.prompt(
            ConfirmPrompt.__name__, PromptOptions(prompt=MessageFactory.text(msg))
        )


    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Complete the interaction and end the dialog."""
        booking_details = step_context.options

        # Capture the results of the previous step
        user_confirmation = step_context.result

        # setup the warning (in case the booking fails)
        CONFIG = DefaultConfig()
        connection_string = f'InstrumentationKey={CONFIG.APPINSIGHTS_INSTRUMENTATION_KEY}'
        logger = logging.getLogger(__name__)
        logger.addHandler(AzureLogHandler(connection_string=connection_string))

        # setup the log (predictions from the bot)
        propreties = step_context.options.__dict__

        if user_confirmation:
            # booking successfull: send log, conclude dialog            
            print('Booking successfull')
            self.telemetry_client.track_event('booking_success', properties=propreties)
            self.telemetry_client.flush()
            return await step_context.end_dialog(booking_details)
        
        # booking unsuccessfull: send log and failure warning, cancel dialog
        print('Booking unsuccessfull')
        self.telemetry_client.track_event('booking_failure', properties=propreties)
        self.telemetry_client.flush()
        logger.warning('warning_booking_failure')
        return await step_context.end_dialog()


    '''
    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Complete the interaction and end the dialog."""
        booking_details = step_context.options

        # Capture the results of the previous step
        user_confirmation = step_context.result
        print(user_confirmation)

        if user_confirmation:
            # booking successfull
            return await step_context.end_dialog(booking_details)
        # booking unsuccessfull
        return await step_context.end_dialog()
    '''


    def is_ambiguous(self, timex: str) -> bool:
        """Ensure time is correct."""
        timex_property = Timex(timex)
        return "definite" not in timex_property.types
