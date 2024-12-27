# ======================================================================================================================

# pylint: disable=line-too-long, missing-class-docstring, missing-function-docstring, missing-module-docstring

import unittest

from tests.base_test_case import BaseTestCase
from tests.error_message import ErrorMessage


# ======================================================================================================================

class EndpointRealizedVolatilityConesTestCase(BaseTestCase):
    # pylint: disable-next=arguments-differ
    def setUp(self):
        super().setUp(
            function_name='get_realized_volatility_cones',
            imprecise_fields=[
                'payload.data[*].current_10days',
                'payload.data[*].current_189days',
                'payload.data[*].current_21days',
                'payload.data[*].current_5days',
                'payload.data[*].current_84days',
                'payload.data[*].max_10days',
                'payload.data[*].max_189days',
                'payload.data[*].max_21days',
                'payload.data[*].max_5days',
                'payload.data[*].max_84days',
                'payload.data[*].min_10days',
                'payload.data[*].min_189days',
                'payload.data[*].min_21days',
                'payload.data[*].min_5days',
                'payload.data[*].min_84days',
                'payload.data[*].p25_10days',
                'payload.data[*].p25_189days',
                'payload.data[*].p25_21days',
                'payload.data[*].p25_5days',
                'payload.data[*].p25_84days',
                'payload.data[*].p50_10days',
                'payload.data[*].p50_189days',
                'payload.data[*].p50_21days',
                'payload.data[*].p50_5days',
                'payload.data[*].p50_84days',
                'payload.data[*].p75_10days',
                'payload.data[*].p75_189days',
                'payload.data[*].p75_21days',
                'payload.data[*].p75_5days',
                'payload.data[*].p75_84days',
            ],
            precision_error=0.00001
        )

    # ==================================================================================================================

    def test_default(self):
        response = self.call_endpoint(currency='MSTR')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=1)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'pair', 'MSTR')

    def test_historical(self):
        response = self.call_endpoint(currency='MSTR', startDate='2024-12-20T00:00:00', endDate='2024-12-21T00:00:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=1)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'pair', 'MSTR')

    # ==================================================================================================================

    def test_invalid_parameter(self):
        response = self.call_endpoint(currency='MSTR', invalid='parameter')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.UNSUPPORTED_PARAMETER_INVALID)

    def test_invalid_exchange(self):
        response = self.call_endpoint(exchange='<exchange>', currency='MSTR')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.UNSUPPORTED_PARAMETER_EXCHANGE)

    def test_invalid_timestamp(self):
        response = self.call_endpoint(currency='MSTR', startDate='<timestamp>')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER_TIMESTAMP)

    # TODO: this endpoint should return 404 instead
    def test_unknown_currency(self):
        response = self.call_endpoint(currency='<currency>')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=1)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'current_10days', None)


# ======================================================================================================================

if __name__ == '__main__':
    unittest.main()

# ======================================================================================================================
