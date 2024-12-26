# ======================================================================================================================

# pylint: disable=line-too-long, missing-class-docstring, missing-function-docstring, missing-module-docstring

import unittest

from tests.base_test_case import BaseTestCase
from tests.error_message import ErrorMessage


# ======================================================================================================================

class EndpointVolatilityTermStructuresConstantTestCase(BaseTestCase):
    # pylint: disable-next=arguments-differ
    def setUp(self):
        super().setUp(function_name='get_volatility_term_structures_constant')

    # ==================================================================================================================

    def test_default(self):
        response = self.call_endpoint(currency='MSTR')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=10)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field_timestamp(response, 'timestamp', is_iso=True) # TODO: this should be 'is_milliseconds=True'

    def test_historical_timeformat_default(self):
        response = self.call_endpoint(currency='MSTR', timestamp='2024-12-01T00:00:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=10)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field_timestamp(response, 'timestamp', is_iso=True) # TODO: this should be 'is_milliseconds=True'

    def test_historical_timeformat_hr(self):
        response = self.call_endpoint(currency='MSTR', timestamp='2024-12-01T00:00:00', timeFormat='hr')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=10)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field_timestamp(response, 'timestamp', is_hr=True)

    def test_historical_timeformat_iso(self):
        response = self.call_endpoint(currency='MSTR', timestamp='2024-12-01T00:00:00', timeFormat='iso')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=10)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field_timestamp(response, 'timestamp', is_iso=True)

    # ==================================================================================================================

    def test_invalid_parameter(self):
        response = self.call_endpoint(currency='MSTR', invalid='parameter')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER)

    def test_invalid_timestamp(self):
        response = self.call_endpoint(currency='MSTR', timestamp='<timestamp>')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER_TIMESTAMP)

    def test_unknown_currency(self):
        response = self.call_endpoint(currency='<currency>')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)

    def test_unknown_exchange(self):
        response = self.call_endpoint(exchange='<exchange>', currency='MSTR')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER_EXCHANGE_TRADFI)



# ======================================================================================================================

if __name__ == '__main__':
    unittest.main()

# ======================================================================================================================
