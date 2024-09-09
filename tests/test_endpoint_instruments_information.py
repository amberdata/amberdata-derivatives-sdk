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
        response = self.call_endpoint(currency='ETH')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response)
        self.validate_response_field(response, 'currency', 'ETH')
        self.validate_response_field_timestamp(response, 'endDate', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'expiration', is_milliseconds=True)

    def test_exchange(self):
        response = self.call_endpoint(exchange='deribit')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field_timestamp(response, 'endDate', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'expiration', is_milliseconds=True)

    def test_putcall(self):
        response = self.call_endpoint(putCall='P')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response)
        self.validate_response_field(response, 'putCall', 'P')
        self.validate_response_field_timestamp(response, 'endDate', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'expiration', is_milliseconds=True)

    def test_strike(self):
        response = self.call_endpoint(strike=5000)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response)
        self.validate_response_field(response, 'strike', 5000)
        self.validate_response_field_timestamp(response, 'endDate', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'expiration', is_milliseconds=True)

    def test_historical_timeformat_default(self):
        response = self.call_endpoint(timestamp='2024-04-01T03:00:00')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=4218)
        self.validate_response_field_timestamp(response, 'endDate', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'expiration', is_milliseconds=True)

    def test_historical_timeformat_hr(self):
        response = self.call_endpoint(timestamp='2024-04-01T03:00:00', timeFormat='hr')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=4218)
        self.validate_response_field_timestamp(response, 'endDate', is_hr=True)
        self.validate_response_field_timestamp(response, 'expiration', is_hr=True)

    def test_historical_timeformat_iso(self):
        response = self.call_endpoint(timestamp='2024-04-01T03:00:00', timeFormat='iso')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=4218)
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

    # TODO: This test should fail, and not return a 500 - validation is missing in data-api
    @unittest.skip("Missing validation")
    def test_invalid_strike(self):
        response = self.call_endpoint(strike='<strike>')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)

    # TODO: This causes a failure in CI: 'tests/fixtures/EndpointInstrumentsInformationTestCase/test_invalid_timeformat.json'
    @unittest.skip("Missing validation")
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
