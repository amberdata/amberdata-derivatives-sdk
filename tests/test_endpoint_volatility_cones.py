# ======================================================================================================================

# pylint: disable=line-too-long, missing-class-docstring, missing-function-docstring, missing-module-docstring

import unittest

from tests.base_test_case import BaseTestCase
from tests.error_message import ErrorMessage


# ======================================================================================================================

class EndpointVolatilityConesTestCase(BaseTestCase):
    def setUp(self, function_name='get_volatility_cones'):
        super().setUp(function_name)

    # ==================================================================================================================

    def test_default(self):
        response = self.call_endpoint(exchange='gdax', pair='btc_usd')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=1)
        self.validate_response_field(response, 'exchange', 'gdax')
        self.validate_response_field(response, 'pair', 'btc_usd')

    def test_historical(self):
        response = self.call_endpoint(exchange='gdax', pair='btc_usd', startDate='2024-04-01T00:00:00', endDate='2024-05-01T00:00:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=1)
        self.validate_response_field(response, 'exchange', 'gdax')
        self.validate_response_field(response, 'pair', 'btc_usd')

    # ==================================================================================================================

    def test_invalid_parameter(self):
        response = self.call_endpoint(exchange='gdax', pair='btc_usd', invalid='parameter')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER)

    def test_invalid_timestamp(self):
        response = self.call_endpoint(exchange='gdax', pair='btc_usd', startDate='<timestamp>')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER_TIMESTAMP)

    # TODO: this endpoint should return 404 instead
    def test_unknown_exchange(self):
        response = self.call_endpoint(exchange='<exchange>', pair='btc_usd')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=1)
        self.validate_response_field(response, 'exchange', '<exchange>')
        self.validate_response_field(response, 'pair', 'btc_usd')
        self.validate_response_field(response, 'current_14days', None)

    # TODO: this endpoint should return 404 instead
    def test_unknown_pair(self):
        response = self.call_endpoint(exchange='gdax', pair='<pair>')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=1)
        self.validate_response_field(response, 'exchange', 'gdax')
        self.validate_response_field(response, 'pair', '<pair>')
        self.validate_response_field(response, 'current_14days', None)


# ======================================================================================================================

if __name__ == '__main__':
    unittest.main()

# ======================================================================================================================
