# ======================================================================================================================

# pylint: disable=line-too-long, missing-class-docstring, missing-function-docstring, missing-module-docstring

import unittest

from tests.base_test_case import BaseTestCase
from tests.error_message import ErrorMessage


# ======================================================================================================================

class EndpointRealizedVolatilityCorrelationBetaTestCase(BaseTestCase):
    def setUp(self, function_name='get_realized_volatility_correlation_beta'):
        super().setUp(function_name)

    # ==================================================================================================================

    def test_default(self):
        response = self.call_endpoint(exchange='gdax', pair='btc_usd', pair2='eth_usd')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=200)
        # TODO: Field exchange should be part of the payload
        # self.validate_response_field(response, 'exchange', 'gdax')
        self.validate_response_field(response, 'pairOne', 'btc_usd')
        self.validate_response_field(response, 'pairTwo', 'eth_usd')
        self.validate_response_field_timestamp(response, 'timestamp', is_milliseconds=True)

    def test_timestamp(self):
        response = self.call_endpoint(exchange='gdax', pair='btc_usd', pair2='eth_usd')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=200)
        # TODO: Field exchange should be part of the payload
        # self.validate_response_field(response, 'exchange', 'gdax')
        self.validate_response_field(response, 'pairOne', 'btc_usd')
        self.validate_response_field(response, 'pairTwo', 'eth_usd')
        self.validate_response_field_timestamp(response, 'timestamp', is_milliseconds=True)

    def test_timestamp_timeformat_hr(self):
        response = self.call_endpoint(exchange='gdax', pair='btc_usd', pair2='eth_usd', timeFormat='hr')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=200)
        # TODO: Field exchange should be part of the payload
        # self.validate_response_field(response, 'exchange', 'gdax')
        self.validate_response_field(response, 'pairOne', 'btc_usd')
        self.validate_response_field(response, 'pairTwo', 'eth_usd')
        self.validate_response_field_timestamp(response, 'timestamp', is_hr=True)

    def test_timestamp_timeformat_iso(self):
        response = self.call_endpoint(exchange='gdax', pair='btc_usd', pair2='eth_usd', timeFormat='iso')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=200)
        # TODO: Field exchange should be part of the payload
        # self.validate_response_field(response, 'exchange', 'gdax')
        self.validate_response_field(response, 'pairOne', 'btc_usd')
        self.validate_response_field(response, 'pairTwo', 'eth_usd')
        self.validate_response_field_timestamp(response, 'timestamp', is_iso=True)

    # ==================================================================================================================

    def test_invalid_parameter(self):
        response = self.call_endpoint(exchange='gdax', pair='btc_usd', pair2='eth_usd', invalid='parameter')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER)

    def test_unknown_exchange(self):
        response = self.call_endpoint(exchange='<exchange>', pair='btc_usd', pair2='eth_usd')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)

    def test_unknown_pair(self):
        response = self.call_endpoint(exchange='gdax', pair='<pair>', pair2='eth_usd')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)

    def test_unknown_pair2(self):
        response = self.call_endpoint(exchange='gdax', pair='btc_usd', pair2='<pair2>')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)


# ======================================================================================================================

if __name__ == '__main__':
    unittest.main()

# ======================================================================================================================
