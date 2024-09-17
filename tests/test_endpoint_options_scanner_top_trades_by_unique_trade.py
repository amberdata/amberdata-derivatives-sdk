# ======================================================================================================================

# pylint: disable=line-too-long, missing-class-docstring, missing-function-docstring, missing-module-docstring, too-many-public-methods

import unittest

from tests.base_test_case import BaseTestCase
from tests.error_message import ErrorMessage


# ======================================================================================================================

class EndpointOptionsScannerTopTradesByUniqueTradeTestCase(BaseTestCase):
    # pylint: disable-next=arguments-differ
    def setUp(self):
        super().setUp(function_name='get_options_scanner_top_trades_by_unique_trade')

    # ==================================================================================================================

    def test_historical(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', uniqueTrade='["sell BTC-27SEP24-90000-C"]', startDate='2024-04-01T00:00:00', endDate='2024-05-01T00:00:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=118)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field(response, 'amberdataDirection', 'sell')
        self.validate_response_field(response, 'instrument', 'BTC-27SEP24-90000-C')
        self.validate_response_field_timestamp(response, 'exchangeTimestamp', is_milliseconds=True)

    def test_historical_blocktradeid(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', uniqueTrade='["sell BTC-27SEP24-90000-C"]', startDate='2024-04-01T00:00:00', endDate='2024-05-01T00:00:00', blockTradeId='BLOCK-138789')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=1)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field(response, 'amberdataDirection', 'sell')
        self.validate_response_field(response, 'instrument', 'BTC-27SEP24-90000-C')
        self.validate_response_field(response, 'blockTradeId', 'BLOCK-138789')
        self.validate_response_field_timestamp(response, 'exchangeTimestamp', is_milliseconds=True)

    def test_historical_blocktradeid_true(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', uniqueTrade='["sell BTC-27SEP24-90000-C"]', startDate='2024-04-01T00:00:00', endDate='2024-05-01T00:00:00', blockTradeId=True)
        self.validate_response_data(response)
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=7)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field(response, 'amberdataDirection', 'sell')
        self.validate_response_field(response, 'instrument', 'BTC-27SEP24-90000-C')
        self.validate_response_field_timestamp(response, 'exchangeTimestamp', is_milliseconds=True)

    def test_historical_blocktradeid_false(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', uniqueTrade='["sell BTC-27SEP24-90000-C"]', startDate='2024-04-01T00:00:00', endDate='2024-05-01T00:00:00', blockTradeId=False)
        self.validate_response_data(response)
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=111)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field(response, 'amberdataDirection', 'sell')
        self.validate_response_field(response, 'instrument', 'BTC-27SEP24-90000-C')
        self.validate_response_field(response, 'blockTradeId', None)
        self.validate_response_field_timestamp(response, 'exchangeTimestamp', is_milliseconds=True)

    def test_historical_timeformat_default(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', uniqueTrade='["sell BTC-27SEP24-90000-C"]', startDate='2024-04-01T00:00:00', endDate='2024-05-01T00:00:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=118)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field(response, 'amberdataDirection', 'sell')
        self.validate_response_field(response, 'instrument', 'BTC-27SEP24-90000-C')
        self.validate_response_field_timestamp(response, 'exchangeTimestamp', is_milliseconds=True)

    def test_historical_timeformat_hr(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', uniqueTrade='["sell BTC-27SEP24-90000-C"]', startDate='2024-04-01T00:00:00', endDate='2024-05-01T00:00:00', timeFormat='hr')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=118)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field(response, 'amberdataDirection', 'sell')
        self.validate_response_field(response, 'instrument', 'BTC-27SEP24-90000-C')
        self.validate_response_field_timestamp(response, 'exchangeTimestamp', is_hr=True)

    def test_historical_timeformat_iso(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', uniqueTrade='["sell BTC-27SEP24-90000-C"]', startDate='2024-04-01T00:00:00', endDate='2024-05-01T00:00:00', timeFormat='iso')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=118)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field(response, 'amberdataDirection', 'sell')
        self.validate_response_field(response, 'instrument', 'BTC-27SEP24-90000-C')
        self.validate_response_field_timestamp(response, 'exchangeTimestamp', is_iso=True)

    # ==================================================================================================================

    def test_invalid_parameter(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', uniqueTrade='["sell BTC-27SEP24-90000-C"]', invalid='parameter')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER)

    def test_invalid_timestamp(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', uniqueTrade='["sell BTC-27SEP24-90000-C"]', startDate='<timestamp>')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER_TIMESTAMP)

    def test_unknown_exchange(self):
        response = self.call_endpoint(exchange='<exchange>', currency='BTC', uniqueTrade='["sell BTC-27SEP24-90000-C"]', )
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)

    def test_unknown_currency(self):
        response = self.call_endpoint(exchange='deribit', currency='<currency>', uniqueTrade='["sell BTC-27SEP24-90000-C"]', )
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)

    def test_unknown_uniquetrade(self):
        response = self.call_endpoint(exchange='deribit', currency='btc', uniqueTrade='<unique_trade>', )
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)


# ======================================================================================================================

if __name__ == '__main__':
    unittest.main()

# ======================================================================================================================
