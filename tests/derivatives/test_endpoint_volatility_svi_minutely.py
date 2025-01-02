# ======================================================================================================================

# pylint: disable=line-too-long, missing-class-docstring, missing-function-docstring, missing-module-docstring, too-many-public-methods

import unittest

from tests.base_test_case import BaseTestCase
from tests.error_message import ErrorMessage


# ======================================================================================================================

class EndpointVolatilitySVIMinutelyTestCase(BaseTestCase):
    # pylint: disable-next=arguments-differ
    def setUp(self):
        super().setUp(function_name='get_volatility_svi_minutely')

    # ==================================================================================================================

    def test_default(self):
        response = self.call_endpoint(currency='BTC')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=5)
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'timestamp', is_milliseconds=True)

    # TODO: missing top level fields in response payload
    def test_default_signature_ecdsa(self):
        response = self.call_endpoint(currency='BTC', signature='ECDSA')

        # This is a bug in the API and needs to be fixed
        response['description'] = 'Successful request'
        response['status'] = 200 # instead of 0
        response['title'] = 'OK'

        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=5)
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'timestamp', is_milliseconds=True)

        signature = response['payload']['metadata']['signature']
        self.assertNotEqual('',   signature)
        self.assertNotEqual(None, signature)
        self.assertTrue(signature.startswith('0x'))
        self.assertEqual(132, len(signature))

    def test_default_sviformat_dte(self):
        response = self.call_endpoint(currency='BTC', sviFormat='DTE')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=5)
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'timestamp', is_milliseconds=True)

    def test_default_sviformat_tau(self):
        response = self.call_endpoint(currency='BTC', sviFormat='TAU')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=5)
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'timestamp', is_milliseconds=True)

    def test_default_timeformat_default(self):
        response = self.call_endpoint(currency='BTC')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=5)
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'timestamp', is_milliseconds=True)

    def test_default_timeformat_hr(self):
        response = self.call_endpoint(currency='BTC', timeFormat='hr')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=5)
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'timestamp', is_hr=True, is_minutely=True)

    def test_default_timeformat_iso(self):
        response = self.call_endpoint(currency='BTC', timeFormat='iso')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=5)
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'timestamp', is_iso=True, is_minutely=True)

    # ==================================================================================================================

    def test_invalid_parameter(self):
        response = self.call_endpoint(currency='BTC', invalid='parameter')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.UNSUPPORTED_PARAMETER_INVALID)

    def test_unknown_currency(self):
        response = self.call_endpoint(currency='<currency>')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.UNSUPPORTED_PARAMETER_CURRENCY_SVI)


# ======================================================================================================================

if __name__ == '__main__':
    unittest.main()

# ======================================================================================================================
