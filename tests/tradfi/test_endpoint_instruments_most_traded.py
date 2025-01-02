# ======================================================================================================================

# pylint: disable=line-too-long, missing-class-docstring, missing-function-docstring, missing-module-docstring

import unittest

from tests.base_test_case import BaseTestCase
from tests.error_message import ErrorMessage


# ======================================================================================================================

class EndpointInstrumentsMostTradedTestCase(BaseTestCase):
    # pylint: disable-next=arguments-differ
    def setUp(self):
        super().setUp(
            function_name    = 'get_instruments_most_traded',
            imprecise_fields = ['payload.data[*].vwapPriceUsd'],
            precision_error  = 0.02,
        )

    # ==================================================================================================================

    def test_default(self):
        response = self.call_endpoint(exchange='tradfi', currency='MSTR', startDate='2024-12-20', endDate='2024-12-21')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=200)

    def test_historical(self):
        response = self.call_endpoint(exchange='tradfi', currency='MSTR', startDate='2024-12-20T00:00:00', endDate='2024-12-21T00:00:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=2939)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')

    # ==================================================================================================================

    def test_invalid_parameter(self):
        response = self.call_endpoint(exchange='tradfi', currency='MSTR', invalid='parameter')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.UNSUPPORTED_PARAMETER_INVALID)

    def test_invalid_timestamp(self):
        response = self.call_endpoint(exchange='tradfi', currency='MSTR', startDate='<timestamp>')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER_TIMESTAMP)

    def test_unknown_currency(self):
        response = self.call_endpoint(exchange='tradfi', currency='<currency>')
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
