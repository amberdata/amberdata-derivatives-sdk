# ======================================================================================================================

# pylint: disable=line-too-long, missing-class-docstring, missing-function-docstring, missing-module-docstring

import unittest

from tests.base_test_case import BaseTestCase
from tests.error_message import ErrorMessage


# ======================================================================================================================

class EndpointFuturesPerpetualsAPRBasisLiveTermStructuresTestCase(BaseTestCase):
    # pylint: disable-next=arguments-differ
    def setUp(self):
        super().setUp(function_name='get_futures_perpetuals_apr_basis_live_term_structures')

    # ==================================================================================================================

    def test_default_margintype_coins(self):
        response = self.call_endpoint(asset='BTC', marginType='coins')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=15)
        self.validate_response_field_timestamp(response, 'expirationTimestamp', is_milliseconds=True)

    def test_default_margintype_stables(self):
        response = self.call_endpoint(asset='BTC', marginType='stables')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=10)
        self.validate_response_field_timestamp(response, 'expirationTimestamp', is_milliseconds=True)

    def test_default_timeformat_default(self):
        response = self.call_endpoint(asset='BTC', marginType='coins')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=15)
        self.validate_response_field_timestamp(response, 'expirationTimestamp', is_milliseconds=True)

    def test_default_timeformat_hr(self):
        response = self.call_endpoint(asset='BTC', marginType='coins', timeFormat='hr')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=15)
        self.validate_response_field_timestamp(response, 'expirationTimestamp', is_hr=True, is_minutely=True)

    def test_historical_timeformat_iso(self):
        response = self.call_endpoint(asset='BTC', marginType='coins', timeFormat='iso')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=15)
        self.validate_response_field_timestamp(response, 'expirationTimestamp', is_iso=True, is_minutely=True)

    # ==================================================================================================================

    def test_invalid_parameter(self):
        response = self.call_endpoint(asset='BTC', marginType='coins', invalid='parameter')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER)

    def test_invalid_margintype(self):
        response = self.call_endpoint(asset='BTC', marginType='<margin_type>')
        self.validate_response_data(response)
        self.validate_response_400(response, message=ErrorMessage.INVALID_PARAMETER_MARGIN_TYPE)

    # TODO: this endpoint should return 404 instead
    def test_unknown_asset(self):
        response = self.call_endpoint(asset='<asset>', marginType='coins')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)


# ======================================================================================================================

if __name__ == '__main__':
    unittest.main()

# ======================================================================================================================
