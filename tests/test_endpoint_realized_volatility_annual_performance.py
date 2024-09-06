# ======================================================================================================================

# pylint: disable=line-too-long, missing-class-docstring, missing-function-docstring, missing-module-docstring

import unittest

from tests.base_test_case import BaseTestCase
from tests.error_message import ErrorMessage


# ======================================================================================================================

class EndpointRealizedVolatilityAnnualPerformanceTestCase(BaseTestCase):
    # pylint: disable-next=arguments-differ
    def setUp(self):
        super().setUp(function_name='get_realized_volatility_annual_performance')

    # ==================================================================================================================

    def test_default(self):
        response = self.call_endpoint(exchange='gdax', pair='btc_usd')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=2000)
        self.validate_response_field(response, 'exchange', 'gdax')
        self.validate_response_field(response, 'pair', 'btc_usd')

    # ==================================================================================================================

    def test_invalid_parameter(self):
        response = self.call_endpoint(exchange='gdax', pair='btc_usd', invalid='parameter')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER)

    # TODO: this endpoint should return 404 instead
    def test_unknown_exchange(self):
        response = self.call_endpoint(exchange='<exchange>', pair='btc_usd')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)
        self.validate_response_field(response, 'exchange', '<exchange>')
        self.validate_response_field(response, 'pair', 'btc_usd')
        self.validate_response_field(response, 'current_14days', None)

    # TODO: this endpoint should return 404 instead
    def test_unknown_pair(self):
        response = self.call_endpoint(exchange='gdax', pair='<pair>')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)
        self.validate_response_field(response, 'exchange', 'gdax')
        self.validate_response_field(response, 'pair', '<pair>')
        self.validate_response_field(response, 'current_14days', None)


# ======================================================================================================================

if __name__ == '__main__':
    unittest.main()

# ======================================================================================================================
