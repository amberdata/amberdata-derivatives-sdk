# pylint: disable=line-too-long, missing-class-docstring, missing-function-docstring, missing-module-docstring

import unittest

from tests.base_test_case import BaseTestCase
from tests.error_message import ErrorMessage


# ======================================================================================================================

class EndpointSpotAnalyticsTradeInformationPairsTestCase(BaseTestCase):
    # pylint: disable-next=arguments-differ
    def setUp(self):
        super().setUp(
            function_name='get_spot_analytics_trade_information_pairs'
        )

    # ==================================================================================================================

    def test_default(self):
        response = self.call_endpoint(exchange='gdax')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=1)
        self.validate_response_field(response, 'exchange', 'gdax')

    # ==================================================================================================================

    def test_invalid_parameter(self):
        response = self.call_endpoint(exchange='gdax', invalid='parameter')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.UNSUPPORTED_PARAMETER_INVALID)

    def test_unknown_exchange(self):
        response = self.call_endpoint(exchange='<exchange>')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)


# ======================================================================================================================

if __name__ == '__main__':
    unittest.main()

# ====================================================================================================================== 