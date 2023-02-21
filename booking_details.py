# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.


class BookingDetails:
    def __init__(
        self,
        #destination: str = None,
        #origin: str = None,
        #travel_date: str = None,
        #unsupported_airports=None,
        or_city: str = None,
        dst_city: str = None,
        str_date: str = None,
        end_date: str = None,
        budget: str = None

    ):
        #if unsupported_airports is None:
        #    unsupported_airports = []
        #self.unsupported_airports = unsupported_airports
        #self.destination = destination
        #self.origin = origin
        #self.travel_date = travel_date
        self.or_city = or_city
        self.dst_city = dst_city
        self.str_date = str_date
        self.end_date = end_date
        self.budget = budget
