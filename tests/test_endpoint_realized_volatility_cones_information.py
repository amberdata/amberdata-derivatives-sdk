# ======================================================================================================================

# pylint: disable=line-too-long, missing-class-docstring, missing-function-docstring, missing-module-docstring

import unittest

from tests.base_test_case import BaseTestCase
from tests.error_message import ErrorMessage


# ======================================================================================================================

class EndpointRealizedVolatilityConesInformationTestCase(BaseTestCase):
    def setUp(self, function_name='get_realized_volatility_cones_information'):
        super().setUp(function_name)

    # ==================================================================================================================

    def test_default(self):
        response = self.call_endpoint(exchange='gdax')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=200)
        self.validate_response_field(response, 'exchange', 'gdax')
        self.validate_response_field_timestamp(response, 'startTimestamp', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'endTimestamp', is_milliseconds=True)

    def test_timestamp(self):
        response = self.call_endpoint(exchange='gdax')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=200)
        self.validate_response_field(response, 'exchange', 'gdax')
        self.validate_response_field_timestamp(response, 'startTimestamp', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'endTimestamp', is_milliseconds=True)

    def test_timestamp_timeformat_hr(self):
        response = self.call_endpoint(exchange='gdax', timeFormat='hr')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=200)
        self.validate_response_field(response, 'exchange', 'gdax')
        self.validate_response_field_timestamp(response, 'startTimestamp', is_hr=True)
        self.validate_response_field_timestamp(response, 'endTimestamp', is_hr=True)

    def test_timestamp_timeformat_iso(self):
        response = self.call_endpoint(exchange='gdax', timeFormat='iso')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=200)
        self.validate_response_field(response, 'exchange', 'gdax')
        self.validate_response_field_timestamp(response, 'startTimestamp', is_iso=True)
        self.validate_response_field_timestamp(response, 'endTimestamp', is_iso=True)

    # ==================================================================================================================

    def test_invalid_parameter(self):
        response = self.call_endpoint(exchange='gdax', invalid='parameter')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER)

    def test_unknown_exchange(self):
        response = self.call_endpoint(exchange='<exchange>')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)


# ======================================================================================================================

if __name__ == '__main__':
    unittest.main()

# ======================================================================================================================
