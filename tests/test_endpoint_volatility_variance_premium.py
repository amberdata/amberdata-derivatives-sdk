# ======================================================================================================================

# pylint: disable=line-too-long, missing-class-docstring, missing-function-docstring, missing-module-docstring

import unittest

from tests.base_test_case import BaseTestCase
from tests.error_message import ErrorMessage


# ======================================================================================================================

class EndpointVolatilityVariancePremiumTestCase(BaseTestCase):
    # pylint: disable-next=arguments-differ
    def setUp(self):
        super().setUp(function_name='get_volatility_variance_premium')

    # ==================================================================================================================

    def test_default(self):
        response = self.call_endpoint(currency='BTC')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=1000)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'instrument', 'btc')
        self.validate_response_field_timestamp(response, 'timestamp', is_milliseconds=True)

    def test_default_timeformat_default(self):
        response = self.call_endpoint(currency='BTC')
        self.validate_response_200(response, min_elements=1000)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'instrument', 'btc')
        self.validate_response_field_timestamp(response, 'timestamp', is_milliseconds=True)

    def test_default_timeformat_hr(self):
        response = self.call_endpoint(currency='BTC', timeFormat='hr')
        self.validate_response_200(response, min_elements=1000)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'instrument', 'btc')
        self.validate_response_field_timestamp(response, 'timestamp', is_hr=True)

    def test_default_timeformat_iso(self):
        response = self.call_endpoint(currency='BTC', timeFormat='iso')
        self.validate_response_200(response, min_elements=1000)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'instrument', 'btc')
        self.validate_response_field_timestamp(response, 'timestamp', is_iso=True)

    # ==================================================================================================================

    def test_invalid_parameter(self):
        response = self.call_endpoint(currency='BTC', invalid='parameter')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER)

    def test_unknown_currency(self):
        response = self.call_endpoint(currency='<currency>')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)


# ======================================================================================================================

if __name__ == '__main__':
    unittest.main()

# ======================================================================================================================
