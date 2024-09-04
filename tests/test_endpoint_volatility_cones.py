# ======================================================================================================================

# pylint: disable=line-too-long, missing-class-docstring, missing-function-docstring, missing-module-docstring

import unittest

from tests.base_test_case import BaseTestCase
from tests.error_message import ErrorMessage


# ======================================================================================================================

class EndpointVolatilityConesTestCase(BaseTestCase):
    # pylint: disable-next=arguments-differ
    def setUp(self):
        super().setUp(
            function_name='get_volatility_cones',
            imprecise_fields=[
                'payload.data[*].current_14days',
                'payload.data[*].current_180days',
                'payload.data[*].current_1day',
                'payload.data[*].current_30days',
                'payload.data[*].current_7days',
                'payload.data[*].current_90days',
                'payload.data[*].max_14days',
                'payload.data[*].max_180days',
                'payload.data[*].max_1day',
                'payload.data[*].max_30days',
                'payload.data[*].max_7days',
                'payload.data[*].max_90days',
                'payload.data[*].min_14days',
                'payload.data[*].min_180days',
                'payload.data[*].min_1day',
                'payload.data[*].min_30days',
                'payload.data[*].min_7days',
                'payload.data[*].min_90days',
                'payload.data[*].p25_14days',
                'payload.data[*].p25_180days',
                'payload.data[*].p25_1day',
                'payload.data[*].p25_30days',
                'payload.data[*].p25_7days',
                'payload.data[*].p25_90days',
                'payload.data[*].p50_14days',
                'payload.data[*].p50_180days',
                'payload.data[*].p50_1day',
                'payload.data[*].p50_30days',
                'payload.data[*].p50_7days',
                'payload.data[*].p50_90days',
                'payload.data[*].p75_14days',
                'payload.data[*].p75_180days',
                'payload.data[*].p75_1day',
                'payload.data[*].p75_30days',
                'payload.data[*].p75_7days',
                'payload.data[*].p75_90days',
            ],
            precision_error=0.00001
        )

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
