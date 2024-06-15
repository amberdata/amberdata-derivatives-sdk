# ======================================================================================================================

import unittest

from .base_test_case import BaseTestCase


# ======================================================================================================================

class EndpointDecoratedTradesTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.schema = self.load_schema('endpoint.decorated_trades.json')

    # ==================================================================================================================

    def test_default(self):
        response = self.amberdata_client.get_decorated_trades(exchange='deribit', currency='BTC')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=500)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'exchangeTimestamp', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'expirationTimestamp', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'postTradeOrderbookTimestamp', is_milliseconds=True, is_nullable=True)
        self.validate_response_field_timestamp(response, 'preTradeOrderbookTimestamp', is_milliseconds=True, is_nullable=True)

    def test_instrument_historical(self):
        response = self.amberdata_client.get_decorated_trades(exchange='deribit', currency='BTC', startDate='2024-04-01T00:00:00', endDate='2024-04-01T00:10:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=163)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'exchangeTimestamp', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'expirationTimestamp', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'postTradeOrderbookTimestamp', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'preTradeOrderbookTimestamp', is_milliseconds=True)

    def test_blocktradeid_historical(self):
        response = self.amberdata_client.get_decorated_trades(exchange='deribit', currency='BTC', blockTradeId=True, startDate='2024-04-01T00:00:00', endDate='2024-04-01T02:00:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=23)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'exchangeTimestamp', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'expirationTimestamp', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'postTradeOrderbookTimestamp', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'preTradeOrderbookTimestamp', is_milliseconds=True)

    def test_putcall_historical(self):
        response = self.amberdata_client.get_decorated_trades(exchange='deribit', currency='BTC', putCall='C', startDate='2024-04-01T00:00:00', endDate='2024-04-01T00:10:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=53)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field(response, 'putCall', 'C')
        self.validate_response_field_timestamp(response, 'exchangeTimestamp', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'expirationTimestamp', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'postTradeOrderbookTimestamp', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'preTradeOrderbookTimestamp', is_milliseconds=True)

    def test_strike_historical(self):
        response = self.amberdata_client.get_decorated_trades(exchange='deribit', currency='BTC', strike=50000, startDate='2024-04-01T00:00:00', endDate='2024-04-02T00:00:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=57)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field(response, 'strike', 50000)
        self.validate_response_field_timestamp(response, 'exchangeTimestamp', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'expirationTimestamp', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'postTradeOrderbookTimestamp', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'preTradeOrderbookTimestamp', is_milliseconds=True)

    def test_timestamp(self):
        response = self.amberdata_client.get_decorated_trades(exchange='deribit', currency='BTC', startDate='2024-04-01T00:00:00', endDate='2024-04-01T00:10:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=163)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'exchangeTimestamp', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'expirationTimestamp', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'postTradeOrderbookTimestamp', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'preTradeOrderbookTimestamp', is_milliseconds=True)

    def test_timestamp_timeformat_hr(self):
        response = self.amberdata_client.get_decorated_trades(exchange='deribit', currency='BTC', startDate='2024-04-01T00:00:00', endDate='2024-04-01T00:10:00', timeFormat='hr')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=163)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'exchangeTimestamp', is_hr=True)
        self.validate_response_field_timestamp(response, 'expirationTimestamp', is_hr=True, is_minutely=True)
        self.validate_response_field_timestamp(response, 'postTradeOrderbookTimestamp', is_hr=True)
        self.validate_response_field_timestamp(response, 'preTradeOrderbookTimestamp', is_hr=True)

    def test_timestamp_timeformat_iso(self):
        response = self.amberdata_client.get_decorated_trades(exchange='deribit', currency='BTC', startDate='2024-04-01T00:00:00', endDate='2024-04-01T00:10:00', timeFormat='iso')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=163)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'exchangeTimestamp', is_iso=True)
        self.validate_response_field_timestamp(response, 'expirationTimestamp', is_iso=True, is_minutely=True)
        self.validate_response_field_timestamp(response, 'postTradeOrderbookTimestamp', is_iso=True)
        self.validate_response_field_timestamp(response, 'preTradeOrderbookTimestamp', is_iso=True)

    # ==================================================================================================================

    def test_invalid_parameter(self):
        response = self.amberdata_client.get_decorated_trades(exchange='deribit', currency='BTC', invalid='parameter')
        self.validate_response_data(response)
        self.validate_response_400(response, "Parameter 'invalid' is not supported.")

    def test_invalid_isatm(self):
        response = self.amberdata_client.get_decorated_trades(exchange='deribit', currency='BTC', isAtm='<is_atm>')
        self.validate_response_data(response)
        self.validate_response_400(response, "Parameter 'isAtm' is not supported.")

    def test_invalid_putcall(self):
        response = self.amberdata_client.get_decorated_trades(exchange='deribit', currency='BTC', putCall='<put_call>')
        self.validate_response_data(response)
        self.validate_response_400(response, "Invalid argument putCall: expected one of [ALL,P,p,put,Put,PUT,C,c,call,Call,CALL], found '<put_call>'.")

    # TODO: This test should fail, and not return a 500 - validation is missing in data-api
    @unittest.skip("Missing validation")
    def test_invalid_strike(self):
        response = self.amberdata_client.get_decorated_trades(exchange='deribit', currency='BTC', strike='<strike>')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)

    def test_invalid_timestamp(self):
        response = self.amberdata_client.get_decorated_trades(exchange='deribit', currency='BTC', startDate='<timestamp>')
        self.validate_response_data(response)
        self.validate_response_400(response, "Invalid timestamp value: '<timestamp>'.")

    def test_unknown_exchange(self):
        response = self.amberdata_client.get_decorated_trades(exchange='<exchange>', currency='BTC')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)

    def test_unknown_currency(self):
        response = self.amberdata_client.get_decorated_trades(exchange='deribit', currency='<currency>')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)


# ======================================================================================================================

if __name__ == '__main__':
    unittest.main()

# ======================================================================================================================
