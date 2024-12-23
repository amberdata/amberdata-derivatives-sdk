# ======================================================================================================================

# pylint: disable=line-too-long, missing-class-docstring, missing-function-docstring, missing-module-docstring

import unittest

from tests.base_test_case import BaseTestCase
from tests.error_message import ErrorMessage


# ======================================================================================================================

class EndpointInstrumentsInformationTestCase(BaseTestCase):
    # pylint: disable-next=arguments-differ
    def setUp(self):
        super().setUp(function_name='get_instruments_information')

    # ==================================================================================================================

    def test_default(self):
        response = self.call_endpoint()
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=1500)
        self.validate_response_field_timestamp(response, 'endDate', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'expiration', is_milliseconds=True)

    def test_currency(self):
        response = self.call_endpoint(currency='MSTR')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=1)
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field_timestamp(response, 'endDate', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'expiration', is_milliseconds=True)

    def test_exchange(self):
        response = self.call_endpoint(exchange='tradfi')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=1)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field_timestamp(response, 'endDate', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'expiration', is_milliseconds=True)

    # TODO: bug in the API
    def test_putcall(self):
        response = self.call_endpoint(timestamp='2024-12-01', putCall='P')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_data(response)
        self.validate_response_200(response, min_elements=1)
        self.validate_response_field(response, 'putCall', 'P')
        self.validate_response_field_timestamp(response, 'endDate', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'expiration', is_milliseconds=True)

    # TODO: bug in the API
    def test_strike(self):
        response = self.call_endpoint(timestamp='2024-12-01', strike=5000)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_data(response)
        self.validate_response_200(response, min_elements=1)
        self.validate_response_field(response, 'strike', 5000)
        self.validate_response_field_timestamp(response, 'endDate', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'expiration', is_milliseconds=True)

    def test_historical_timeformat_default(self):
        response = self.call_endpoint(timestamp='2024-12-01')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=17988)
        self.validate_response_field_timestamp(response, 'endDate', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'expiration', is_milliseconds=True)

    def test_historical_timeformat_hr(self):
        response = self.call_endpoint(timestamp='2024-12-01', timeFormat='hr')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=17988)
        self.validate_response_field_timestamp(response, 'endDate', is_hr=True)
        self.validate_response_field_timestamp(response, 'expiration', is_hr=True)

    def test_historical_timeformat_iso(self):
        response = self.call_endpoint(timestamp='2024-12-01', timeFormat='iso')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=17988)
        self.validate_response_field_timestamp(response, 'endDate', is_iso=True)
        self.validate_response_field_timestamp(response, 'expiration', is_iso=True)

    # ==================================================================================================================

    def test_invalid_parameter(self):
        response = self.call_endpoint(invalid='parameter')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER)

    def test_invalid_putcall(self):
        response = self.call_endpoint(putCall='<put_call>')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER_PUT_CALL)

    def test_invalid_strike(self):
        response = self.call_endpoint(strike='<strike>')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER_STRIKE)

    def test_invalid_timeformat(self):
        response = self.call_endpoint(timeFormat='<time_format>')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER_TIME_FORMAT)

    def test_invalid_timestamp(self):
        response = self.call_endpoint(timestamp='<timestamp>')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER_TIMESTAMP)

    def test_unknown_currency(self):
        response = self.call_endpoint(currency='<currency>')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)

    def test_unknown_exchange(self):
        response = self.call_endpoint(exchange='<exchange>')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)


# ======================================================================================================================

if __name__ == '__main__':
    unittest.main()

# ======================================================================================================================
