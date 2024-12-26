# ======================================================================================================================

# pylint: disable=line-too-long, missing-class-docstring, missing-function-docstring, missing-module-docstring, too-many-public-methods

import unittest

from tests.base_test_case import BaseTestCase
from tests.error_message import ErrorMessage


# ======================================================================================================================

class EndpointVolatilityLevel1QuotesTestCase(BaseTestCase):
    # pylint: disable-next=arguments-differ
    def setUp(self):
        super().setUp(function_name='get_volatility_level_1_quotes')

    # ==================================================================================================================

    def test_default(self):
        response = self.call_endpoint(currency='MSTR')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=50)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field_timestamp(response, 'timestamp', is_iso=True) # TODO: this should be 'is_milliseconds=True'

    def test_historical(self):
        response = self.call_endpoint(currency='MSTU', instrument='MSTU-27DEC24-1-P', startDate='2024-12-23T17:00:00', endDate='2024-12-23T18:00:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=13)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTU')
        self.validate_response_field(response, 'instrument', 'MSTU-27DEC24-1-P')
        self.validate_response_field_timestamp(response, 'timestamp', is_iso=True) # TODO: this should be 'is_milliseconds=True'

    def test_historical_isatm(self):
        response = self.call_endpoint(currency='MSTU', isAtm=True, startDate='2024-12-23T17:00:00', endDate='2024-12-23T18:00:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=234)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTU')
        self.validate_response_field(response, 'isAtm', True)
        self.validate_response_field_timestamp(response, 'timestamp', is_iso=True) # TODO: this should be 'is_milliseconds=True'

    def test_realtime_isatm(self):
        response = self.call_endpoint(currency='MSTU', isAtm=False)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=25)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTU')
        self.validate_response_field(response, 'isAtm', False)
        self.validate_response_field_timestamp(response, 'timestamp', is_iso=True) # TODO: this should be 'is_milliseconds=True'

    # TODO: Parameter 'putCall' is not supported.
    # def test_historical_putcall(self):
    #     response = self.call_endpoint(currency='MSTU', putCall='C', startDate='2024-12-23T17:00:00', endDate='2024-12-23T18:00:00')
    #     self.validate_response_data(response)
    #     self.validate_response_schema(response, schema=self.schema)
    #     self.validate_response_200(response, num_elements=5320)
    #     self.validate_response_field(response, 'exchange', 'tradfi')
    #     self.validate_response_field(response, 'currency', 'MSTU')
    #     self.validate_response_field(response, 'putCall', 'C')
    #     self.validate_response_field_timestamp(response, 'timestamp', is_iso=True) # TODO: this should be 'is_milliseconds=True'

    # TODO: Parameter 'putCall' is not supported.
    # def test_realtime_putcall(self):
    #     response = self.call_endpoint(currency='MSTU', putCall='P')
    #     self.validate_response_schema(response, schema=self.schema)
    #     self.validate_response_200(response, min_elements=25)
    #     self.validate_response_field(response, 'exchange', 'tradfi')
    #     self.validate_response_field(response, 'currency', 'MSTU')
    #     self.validate_response_field(response, 'putCall', 'P')
    #     self.validate_response_field_timestamp(response, 'timestamp', is_iso=True) # TODO: this should be 'is_milliseconds=True'

    def test_historical_strike(self):
        response = self.call_endpoint(currency='MSTU', strike=2, startDate='2024-12-23T17:00:00', endDate='2024-12-23T18:00:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=234)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTU')
        self.validate_response_field(response, 'strike', 2)
        self.validate_response_field_timestamp(response, 'timestamp', is_iso=True) # TODO: this should be 'is_milliseconds=True'

    def test_realtime_strike(self):
        response = self.call_endpoint(currency='MSTU', strike=2)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=1)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTU')
        self.validate_response_field(response, 'strike', 2)
        self.validate_response_field_timestamp(response, 'timestamp', is_iso=True) # TODO: this should be 'is_milliseconds=True'

    def test_historical_timeformat_default(self):
        response = self.call_endpoint(currency='MSTU', startDate='2024-12-23T17:00:00', endDate='2024-12-23T17:01:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=2552)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTU')
        self.validate_response_field_timestamp(response, 'timestamp', is_iso=True) # TODO: this should be 'is_milliseconds=True'

    def test_historical_timeformat_hr(self):
        response = self.call_endpoint(currency='MSTU', startDate='2024-12-23T17:00:00', endDate='2024-12-23T17:01:00', timeFormat='hr')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=2552)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTU')
        self.validate_response_field_timestamp(response, 'timestamp', is_hr=True, is_minutely=True)

    def test_historical_timeformat_iso(self):
        response = self.call_endpoint(currency='MSTU', startDate='2024-12-23T17:00:00', endDate='2024-12-23T17:01:00', timeFormat='iso')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=2552)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTU')
        self.validate_response_field_timestamp(response, 'timestamp', is_iso=True, is_minutely=True)

    # TODO: parameter timeInterval=d does not return any data
    def test_historical_timeinterval_days(self):
        response = self.call_endpoint(currency='MSTU', startDate='2024-11-29T00:00:00', endDate='2024-12-25T00:00:00', timeFormat='hr', timeInterval='d')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=1064)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTU')
        self.validate_response_field_timestamp(response, 'timestamp', is_hr=True, is_daily=True)

    def test_historical_timeinterval_hours(self):
        response = self.call_endpoint(currency='MSTU', startDate='2024-12-23T17:00:00', endDate='2024-12-23T18:00:00', timeFormat='hr', timeInterval='h')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=5104)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTU')
        self.validate_response_field_timestamp(response, 'timestamp', is_hr=True, is_hourly=True)

    def test_historical_timeinterval_minutes(self):
        response = self.call_endpoint(currency='MSTU', startDate='2024-12-23T17:00:00', endDate='2024-12-23T17:01:00', timeFormat='hr', timeInterval='m')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=2552)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTU')
        self.validate_response_field_timestamp(response, 'timestamp', is_hr=True, is_minutely=True)

    # ==================================================================================================================

    def test_invalid_parameter(self):
        response = self.call_endpoint(currency='MSTR', invalid='parameter')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER)

    def test_invalid_exchange(self):
        response = self.call_endpoint(exchange='<exchange>', currency='MSTR')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.UNSUPPORTED_EXCHANGE)

    def test_invalid_isatm(self):
        response = self.call_endpoint(currency='MSTR', isAtm='<is_atm>')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER_IS_ATM)

    def test_invalid_strike(self):
        response = self.call_endpoint(currency='MSTR', strike='<strike>')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER_STRIKE)

    def test_invalid_timestamp(self):
        response = self.call_endpoint(currency='MSTR', startDate='<timestamp>')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER_TIMESTAMP)

    def test_unknown_currency(self):
        response = self.call_endpoint(currency='<currency>')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)


# ======================================================================================================================

if __name__ == '__main__':
    unittest.main()

# ======================================================================================================================
