# ======================================================================================================================

# pylint: disable=line-too-long, missing-class-docstring, missing-function-docstring, missing-module-docstring

import unittest

from tests.base_test_case import BaseTestCase
from tests.error_message import ErrorMessage


# ======================================================================================================================

class EndpointTradesFlowOptionsYieldsTestCase(BaseTestCase):
    # pylint: disable-next=arguments-differ
    def setUp(self):
        super().setUp(
            function_name='get_trades_flow_options_yields',
            time_format=None
        )

    # ==================================================================================================================

    def test_default(self):
        response = self.call_endpoint(currency='MSTR')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=20)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field_timestamp(response, 'timestamp', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'expirationTimestamp', is_milliseconds=True)

    def test_timeformat_default(self):
        response = self.call_endpoint(currency='MSTR')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=20)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field_timestamp(response, 'timestamp', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'expirationTimestamp', is_milliseconds=True)

    def test_timeformat_hr(self):
        response = self.call_endpoint(currency='MSTR', timeFormat='hr')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=20)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field_timestamp(response, 'timestamp', is_hr=True)
        self.validate_response_field_timestamp(response, 'expirationTimestamp', is_hr=True)

    def test_timeformat_iso(self):
        response = self.call_endpoint(currency='MSTR', timeFormat='iso')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=20)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field_timestamp(response, 'timestamp', is_iso=True)
        self.validate_response_field_timestamp(response, 'expirationTimestamp', is_iso=True)

    # ==================================================================================================================

    def test_invalid_parameter(self):
        response = self.call_endpoint(currency='MSTR', invalid='parameter')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.UNSUPPORTED_PARAMETER_INVALID)

    def test_invalid_exchange(self):
        response = self.call_endpoint(exchange='<exchange>', currency='MSTR')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.UNSUPPORTED_PARAMETER_EXCHANGE)

    def test_unknown_currency(self):
        response = self.call_endpoint(currency='<currency>')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)


# ======================================================================================================================

if __name__ == '__main__':
    unittest.main()

# ======================================================================================================================
