# ======================================================================================================================

# pylint: disable=line-too-long, missing-class-docstring, missing-function-docstring, missing-module-docstring

import unittest

from tests.base_test_case import BaseTestCase
from tests.error_message import ErrorMessage


# ======================================================================================================================

class EndpointRealizedVolatilitySeasonalityMonthOfYearTestCase(BaseTestCase):
    def setUp(self, function_name='get_realized_volatility_seasonality_month_of_year'):
        super().setUp(function_name)

    # ==================================================================================================================

    def test_default(self):
        response = self.call_endpoint(exchange='gdax', pair='btc_usd')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=12)

    def test_instrument_historical(self):
        response = self.call_endpoint(exchange='gdax', pair='btc_usd', startDate='2023-06-01T00:00:00', endDate='2024-06-01T00:10:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=12)

    # ==================================================================================================================

    def test_invalid_parameter(self):
        response = self.call_endpoint(exchange='gdax',pair='btc_usd', invalid='parameter')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER)

    def test_unknown_exchange(self):
        response = self.call_endpoint(exchange='<exchange>', pair='btc_usd')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)

    def test_unknown_pair(self):
        response = self.call_endpoint(exchange='gdax', pair='<pair>')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)


# ======================================================================================================================

if __name__ == '__main__':
    unittest.main()

# ======================================================================================================================
