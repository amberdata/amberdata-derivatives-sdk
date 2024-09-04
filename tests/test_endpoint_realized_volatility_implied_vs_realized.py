# ======================================================================================================================

# pylint: disable=line-too-long, missing-class-docstring, missing-function-docstring, missing-module-docstring

import unittest

from tests.base_test_case import BaseTestCase
from tests.error_message import ErrorMessage


# ======================================================================================================================

class EndpointRealizedVolatilityImpliedVsRealizedTestCase(BaseTestCase):
    def setUp(self, function_name: str = None, time_format: str = None, ignore_fields: list = None):
        super().setUp(
            function_name='get_realized_volatility_implied_vs_realized',
            imprecise_fields=[
                'payload.data[*].realizedVolatility7',
                'payload.data[*].realizedVolatility30',
            ],
            precision_error=0.05
        )

    # ==================================================================================================================

    def test_default(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=8000)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'timestamp', is_milliseconds=True)

    def test_historical(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', startDate='2024-04-01T00:00:00', endDate='2024-05-01T00:00:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=720)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'timestamp', is_milliseconds=True)

    # ==================================================================================================================

    def test_invalid_parameter(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', invalid='parameter')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER)

    def test_invalid_timestamp(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', startDate='<timestamp>')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER_TIMESTAMP)

    # # TODO: this endpoint should return 404 instead
    def test_unknown_exchange(self):
        response = self.call_endpoint(exchange='<exchange>', currency='BTC')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)

    # # TODO: this endpoint should return 404 instead
    def test_unknown_pair(self):
        response = self.call_endpoint(exchange='deribit', currency='<currency>')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)


# ======================================================================================================================

if __name__ == '__main__':
    unittest.main()

# ======================================================================================================================
