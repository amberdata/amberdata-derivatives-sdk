# ======================================================================================================================

# pylint: disable=line-too-long, missing-class-docstring, missing-function-docstring, missing-module-docstring

import unittest

from tests.base_test_case import BaseTestCase
from tests.error_message import ErrorMessage


# ======================================================================================================================

class EndpointTradesFlowPutCallDistributionTestCase(BaseTestCase):
    # pylint: disable-next=arguments-differ
    def setUp(self):
        super().setUp(
            function_name='get_trades_flow_put_call_distribution',
            imprecise_fields=[
                'payload.data[*].callsContractsBought',
                'payload.data[*].callsContractsBoughtExchangeDirection',
                'payload.data[*].callsContractsSold',
                'payload.data[*].callsContractsSoldExchangeDirection',
                'payload.data[*].callsPremiumBought',
                'payload.data[*].callsPremiumBoughtExchangeDirection',
                'payload.data[*].callsPremiumSold',
                'payload.data[*].callsPremiumSoldExchangeDirection',
                'payload.data[*].notionalVolumeOnScreen',
                'payload.data[*].premiumVolumeOnScreen',
                'payload.data[*].putContractsBought',
                'payload.data[*].putContractsBoughtExchangeDirection',
                'payload.data[*].putContractsSold',
                'payload.data[*].putContractsSoldExchangeDirection',
                'payload.data[*].putPremiumBought',
                'payload.data[*].putPremiumBoughtExchangeDirection',
                'payload.data[*].putPremiumSold',
                'payload.data[*].putPremiumSoldExchangeDirection'
            ]
        )

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
        response = self.call_endpoint(exchange='deribit', currency='BTC', startDate='2024-04-01T00:00:00', endDate='2024-05-01T00:00:00', expiration='2024-04-15T08:00:00')
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

    def test_unknown_currency(self):
        response = self.call_endpoint(exchange='deribit', currency='<currency>')
        # TODO: API should return 404 instead
        # self.validate_response_data(response)
        self.validate_response_200(response, num_elements=1)
        self.validate_response_field(response, 'callsContractsBought', 0)
        self.validate_response_field(response, 'callsContractsBoughtExchangeDirection', 0)
        self.validate_response_field(response, 'callsContractsSold', 0)
        self.validate_response_field(response, 'callsContractsSoldExchangeDirection', 0)
        self.validate_response_field(response, 'callsPremiumBought', 0)
        self.validate_response_field(response, 'callsPremiumBoughtExchangeDirection', 0)
        self.validate_response_field(response, 'callsPremiumSold', 0)
        self.validate_response_field(response, 'callsPremiumSoldExchangeDirection', 0)
        self.validate_response_field(response, 'putContractsBought', 0)
        self.validate_response_field(response, 'putContractsBoughtExchangeDirection', 0)
        self.validate_response_field(response, 'putContractsSold', 0)
        self.validate_response_field(response, 'putContractsSoldExchangeDirection', 0)
        self.validate_response_field(response, 'putPremiumBought', 0)
        self.validate_response_field(response, 'putPremiumBoughtExchangeDirection', 0)
        self.validate_response_field(response, 'putPremiumSold', 0)
        self.validate_response_field(response, 'putPremiumSoldExchangeDirection', 0)


# ======================================================================================================================

if __name__ == '__main__':
    unittest.main()

# ======================================================================================================================
