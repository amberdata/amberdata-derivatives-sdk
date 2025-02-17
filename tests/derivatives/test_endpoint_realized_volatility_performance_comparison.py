# ======================================================================================================================

# pylint: disable=line-too-long, missing-class-docstring, missing-function-docstring, missing-module-docstring

import unittest

from tests.base_test_case import BaseTestCase
from tests.error_message import ErrorMessage


# ======================================================================================================================

class EndpointRealizedVolatilityPerformanceComparisonTestCase(BaseTestCase):
    # pylint: disable-next=arguments-differ
    def setUp(self):
        super().setUp(function_name='get_realized_volatility_performance_comparison')

    # ==================================================================================================================

    def test_default(self):
        response = self.call_endpoint(exchange='gdax', pair='btc_usd', pair2='eth_usd')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=2500)
        self.validate_response_field(response, 'exchange', 'gdax')
        self.validate_response_field(response, 'pair', 'btc_usd', 'eth_usd')
        self.validate_response_field_timestamp(response, 'timestamp', is_milliseconds=True)

    def test_historical(self):
        response = self.call_endpoint(exchange='gdax', pair='btc_usd', pair2='eth_usd', startDate='2024-04-01T00:00:00', endDate='2024-05-01T00:00:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=60)
        self.validate_response_field(response, 'exchange', 'gdax')
        self.validate_response_field(response, 'pair', 'btc_usd', 'eth_usd')
        self.validate_response_field_timestamp(response, 'timestamp', is_milliseconds=True, is_daily=True)

    def test_historical_timeformat_default(self):
        response = self.call_endpoint(exchange='gdax', pair='btc_usd', pair2='eth_usd', startDate='2024-04-01T00:00:00', endDate='2024-05-01T00:00:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=60)
        self.validate_response_field(response, 'exchange', 'gdax')
        self.validate_response_field(response, 'pair', 'btc_usd', 'eth_usd')
        self.validate_response_field_timestamp(response, 'timestamp', is_milliseconds=True, is_daily=True)

    def test_historical_timeformat_hr(self):
        response = self.call_endpoint(exchange='gdax', pair='btc_usd', pair2='eth_usd', startDate='2024-04-01T00:00:00', endDate='2024-05-01T00:00:00', timeFormat='hr')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=60)
        self.validate_response_field(response, 'exchange', 'gdax')
        self.validate_response_field(response, 'pair', 'btc_usd', 'eth_usd')
        self.validate_response_field_timestamp(response, 'timestamp', is_hr=True, is_daily=True)

    def test_historical_timeformat_iso(self):
        response = self.call_endpoint(exchange='gdax', pair='btc_usd', pair2='eth_usd', startDate='2024-04-01T00:00:00', endDate='2024-05-01T00:00:00', timeFormat='iso')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=60)
        self.validate_response_field(response, 'exchange', 'gdax')
        self.validate_response_field(response, 'pair', 'btc_usd', 'eth_usd')
        self.validate_response_field_timestamp(response, 'timestamp', is_iso=True, is_daily=True)

    # ==================================================================================================================

    def test_invalid_parameter(self):
        response = self.call_endpoint(exchange='gdax', pair='btc_usd', pair2='eth_usd', invalid='parameter')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.UNSUPPORTED_PARAMETER_INVALID)

    def test_invalid_timestamp(self):
        response = self.call_endpoint(exchange='gdax', pair='btc_usd', pair2='eth_usd', startDate='<timestamp>')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER_TIMESTAMP)

    # TODO: this endpoint should return 404 instead
    def test_unknown_exchange(self):
        response = self.call_endpoint(exchange='<exchange>', pair='btc_usd', pair2='eth_usd')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)
        self.validate_response_field(response, 'exchange', '<exchange>')
        self.validate_response_field(response, 'pair', 'btc_usd', 'eth_usd')

    # TODO: this endpoint should return 404 instead
    def test_unknown_pair(self):
        response = self.call_endpoint(exchange='gdax', pair='btc_usd', pair2='<pair>', startDate='2024-04-01T00:00:00', endDate='2024-05-01T00:00:00', timeFormat='hr')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=30)
        self.validate_response_field(response, 'exchange', 'gdax')
        self.validate_response_field(response, 'pair', 'btc_usd')

    # TODO: this endpoint should return 404 instead
    def test_unknown_pair2(self):
        response = self.call_endpoint(exchange='gdax', pair='<pair>', pair2='eth_usd', startDate='2024-04-01T00:00:00', endDate='2024-05-01T00:00:00', timeFormat='hr')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=30)
        self.validate_response_field(response, 'exchange', 'gdax')
        self.validate_response_field(response, 'pair', 'eth_usd')


# ======================================================================================================================

if __name__ == '__main__':
    unittest.main()

# ======================================================================================================================
