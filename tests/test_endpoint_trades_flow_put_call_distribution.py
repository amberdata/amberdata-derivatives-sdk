# ======================================================================================================================

# pylint: disable=line-too-long, missing-class-docstring, missing-function-docstring, missing-module-docstring

import unittest

from tests.base_test_case import BaseTestCase
from tests.error_message import ErrorMessage


# ======================================================================================================================

class EndpointTradesFlowPutCallDistributionTestCase(BaseTestCase):
    def setUp(self, function_name='get_trades_flow_put_call_distribution'):
        super().setUp(function_name)

    # ==================================================================================================================

    def test_default(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=1)

    def test_default_blocktradeid_true(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', blockTradeId=True)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=1)
        response = self.call_endpoint(exchange='deribit', currency='BTC', blockTradeId=True)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=1)

    def test_default_blocktradeid_false(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', blockTradeId=False)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=1)

    def test_historical(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', startDate='2024-04-01T00:00:00', endDate='2024-04-01T00:10:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=1)

    def test_historical_blocktradeid_true(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', startDate='2024-04-01T00:00:00', endDate='2024-04-10T00:00:00', blockTradeId=True)
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=1)

    def test_historical_blocktradeid_false(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', startDate='2024-04-01T00:00:00', endDate='2024-04-10T00:00:00', blockTradeId=False)
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=1)

    def test_historical_expiration(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', startDate='2024-04-01T00:00:00', endDate='2024-05-01T00:00:00', expiration='2024-04-15 08:00:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=1)

    def test_historical_strike(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', startDate='2024-04-01T00:00:00', endDate='2024-04-10T00:00:00', strike='50000')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=1)

    # ==================================================================================================================

    def test_invalid_parameter(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', invalid='parameter')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER)

    # TODO: This test should fail - validation is missing in data-api
    @unittest.skip("Missing validation")
    def test_invalid_expiration(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', expiration='<expiration>')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER_TIMESTAMP)

    def test_invalid_timestamp(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', startDate='<timestamp>')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER_TIMESTAMP)

    def test_unknown_exchange(self):
        response = self.call_endpoint(exchange='<exchange>', currency='BTC')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=1)
        self.validate_response_field(response, 'callsContractsBought', None)
        self.validate_response_field(response, 'callsContractsBoughtExchangeDirection', None)
        self.validate_response_field(response, 'callsContractsSold', None)
        self.validate_response_field(response, 'callsContractsSoldExchangeDirection', None)
        self.validate_response_field(response, 'callsPremiumBought', None)
        self.validate_response_field(response, 'callsPremiumBoughtExchangeDirection', None)
        self.validate_response_field(response, 'callsPremiumSold', None)
        self.validate_response_field(response, 'callsPremiumSoldExchangeDirection', None)
        self.validate_response_field(response, 'putContractsBought', None)
        self.validate_response_field(response, 'putContractsBoughtExchangeDirection', None)
        self.validate_response_field(response, 'putContractsSold', None)
        self.validate_response_field(response, 'putContractsSoldExchangeDirection', None)
        self.validate_response_field(response, 'putPremiumBought', None)
        self.validate_response_field(response, 'putPremiumBoughtExchangeDirection', None)
        self.validate_response_field(response, 'putPremiumSold', None)
        self.validate_response_field(response, 'putPremiumSoldExchangeDirection', None)

    def test_unknown_currency(self):
        response = self.call_endpoint(exchange='deribit', currency='<currency>')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=1)
        self.validate_response_field(response, 'callsContractsBought', None)
        self.validate_response_field(response, 'callsContractsBoughtExchangeDirection', None)
        self.validate_response_field(response, 'callsContractsSold', None)
        self.validate_response_field(response, 'callsContractsSoldExchangeDirection', None)
        self.validate_response_field(response, 'callsPremiumBought', None)
        self.validate_response_field(response, 'callsPremiumBoughtExchangeDirection', None)
        self.validate_response_field(response, 'callsPremiumSold', None)
        self.validate_response_field(response, 'callsPremiumSoldExchangeDirection', None)
        self.validate_response_field(response, 'putContractsBought', None)
        self.validate_response_field(response, 'putContractsBoughtExchangeDirection', None)
        self.validate_response_field(response, 'putContractsSold', None)
        self.validate_response_field(response, 'putContractsSoldExchangeDirection', None)
        self.validate_response_field(response, 'putPremiumBought', None)
        self.validate_response_field(response, 'putPremiumBoughtExchangeDirection', None)
        self.validate_response_field(response, 'putPremiumSold', None)
        self.validate_response_field(response, 'putPremiumSoldExchangeDirection', None)


# ======================================================================================================================

if __name__ == '__main__':
    unittest.main()

# ======================================================================================================================
