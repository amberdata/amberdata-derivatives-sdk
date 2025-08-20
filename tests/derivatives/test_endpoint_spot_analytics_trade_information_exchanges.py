# pylint: disable=line-too-long, missing-class-docstring, missing-function-docstring, missing-module-docstring

import unittest

from tests.base_test_case import BaseTestCase
from tests.error_message import ErrorMessage


# ======================================================================================================================

class EndpointSpotAnalyticsTradeInformationExchangesTestCase(BaseTestCase):
    # pylint: disable-next=arguments-differ
    def setUp(self):
        super().setUp(
            function_name='get_spot_analytics_trade_information_exchanges'
        )

    # ==================================================================================================================

    def test_default(self):
        response = self.call_endpoint(pair='BTC_USD')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=1)
        self.validate_response_field(response, 'pair', 'BTC_USD')

    # ==================================================================================================================

    def test_invalid_parameter(self):
        response = self.call_endpoint(pair='BTC_USD', invalid='parameter')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.UNSUPPORTED_PARAMETER_INVALID)

    def test_unknown_pair(self):
        response = self.call_endpoint(pair='<pair>')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)


# ======================================================================================================================

if __name__ == '__main__':
    unittest.main()

# ====================================================================================================================== 