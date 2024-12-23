# ======================================================================================================================

# pylint: disable=line-too-long, missing-class-docstring, missing-function-docstring, missing-module-docstring

import unittest

from tests.base_test_case import BaseTestCase
from tests.error_message import ErrorMessage


# ======================================================================================================================

class EndpointTradesFlowDecoratedTradesTestCase(BaseTestCase):
    # pylint: disable-next=arguments-differ
    def setUp(self):
        super().setUp(function_name='get_trades_flow_decorated_trades')

    # ==================================================================================================================

    # TODO: API returns nothing on the week-ends
    def test_default(self):
        response = self.call_endpoint(currency='MSTR')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=500)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field_timestamp(response, 'exchangeTimestamp', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'expirationTimestamp', is_milliseconds=True)

    def test_historical(self):
        response = self.call_endpoint(currency='MSTR', startDate='2024-12-20T15:00:00', endDate='2024-12-20T15:01:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=445)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field_timestamp(response, 'exchangeTimestamp', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'expirationTimestamp', is_milliseconds=True)

    # TODO: bug in the API
    def test_historical_putcall(self):
        response = self.call_endpoint(currency='MSTR', putCall='C', startDate='2024-12-20T15:00:00', endDate='2024-12-20T15:01:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=237)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field(response, 'putCall', 'C')
        self.validate_response_field_timestamp(response, 'exchangeTimestamp', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'expirationTimestamp', is_milliseconds=True)

    def test_historical_strike(self):
        response = self.call_endpoint(currency='MSTR', strike=420, startDate='2024-12-20T15:00:00', endDate='2024-12-20T15:01:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=11)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field(response, 'strike', 420)
        self.validate_response_field_timestamp(response, 'exchangeTimestamp', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'expirationTimestamp', is_milliseconds=True)

    def test_historical_timeformat_default(self):
        response = self.call_endpoint(currency='MSTR', startDate='2024-12-20T15:00:00', endDate='2024-12-20T15:01:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=445)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field_timestamp(response, 'exchangeTimestamp', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'expirationTimestamp', is_milliseconds=True)

    def test_historical_timeformat_hr(self):
        response = self.call_endpoint(currency='MSTR', startDate='2024-12-20T15:00:00', endDate='2024-12-20T15:01:00', timeFormat='hr')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=445)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field_timestamp(response, 'exchangeTimestamp', is_hr=True)
        self.validate_response_field_timestamp(response, 'expirationTimestamp', is_hr=True, is_minutely=True)

    def test_historical_timeformat_iso(self):
        response = self.call_endpoint(currency='MSTR', startDate='2024-12-20T15:00:00', endDate='2024-12-20T15:01:00', timeFormat='iso')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=445)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field_timestamp(response, 'exchangeTimestamp', is_iso=True)
        self.validate_response_field_timestamp(response, 'expirationTimestamp', is_iso=True, is_minutely=True)

    # ==================================================================================================================

    def test_invalid_parameter(self):
        response = self.call_endpoint(currency='MSTR', invalid='parameter')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER)

    def test_invalid_exchange(self):
        response = self.call_endpoint(exchange='<exchange>', currency='BTC')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.UNSUPPORTED_EXCHANGE)

    def test_invalid_isatm(self):
        response = self.call_endpoint(currency='MSTR', isAtm='<is_atm>')
        self.validate_response_data(response)
        self.validate_response_400(response, "Parameter 'isAtm' is not supported.")

    def test_invalid_putcall(self):
        response = self.call_endpoint(currency='MSTR', putCall='<put_call>')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER_PUT_CALL)

    def test_invalid_strike(self):
        response = self.call_endpoint(currency='MSTR', strike='<strike>')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER_STRIKE)

    def test_invalid_timestamp(self):
        response = self.call_endpoint(currency='MSTR', startDate='<timestamp>')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER_TIMESTAMP)

    def test_unknown_currency(self):
        response = self.call_endpoint(currency='<currency>')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)


# ======================================================================================================================

if __name__ == '__main__':
    unittest.main()

# ======================================================================================================================
