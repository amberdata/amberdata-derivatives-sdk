# ======================================================================================================================

# pylint: disable=line-too-long, missing-class-docstring, missing-function-docstring, missing-module-docstring

import unittest

from tests.base_test_case import BaseTestCase
from tests.error_message import ErrorMessage


# ======================================================================================================================

class EndpointTradesFlowNetVolumesTestCase(BaseTestCase):
    def setUp(self, function_name='get_trades_flow_net_volumes'):
        super().setUp(function_name)

    # ==================================================================================================================

    def test_default(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=500)
        self.validate_response_field_timestamp(response, 'timestamp', is_milliseconds=True)

    def test_historical(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', startDate='2024-04-01T00:00:00', endDate='2024-04-01T00:10:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=2280)
        self.validate_response_field_timestamp(response, 'timestamp', is_milliseconds=True)

    def test_historical_blocktradeid_true(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', blockTradeId=True, startDate='2024-04-01T00:00:00', endDate='2024-04-01T02:00:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=528)
        self.validate_response_field_timestamp(response, 'timestamp', is_milliseconds=True)

    def test_historical_blocktradeid_false(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', blockTradeId=False, startDate='2024-04-01T00:00:00', endDate='2024-04-01T02:00:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=2280)
        self.validate_response_field_timestamp(response, 'timestamp', is_milliseconds=True)

    def test_historical_timeformat_default(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', startDate='2024-04-01T00:00:00', endDate='2024-04-01T00:10:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=2280)
        self.validate_response_field_timestamp(response, 'timestamp', is_milliseconds=True)

    def test_historical_timeformat_hr(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', startDate='2024-04-01T00:00:00', endDate='2024-04-01T00:10:00', timeFormat='hr')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=2280)
        self.validate_response_field_timestamp(response, 'timestamp', is_hr=True)

    def test_historical_timeformat_iso(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', startDate='2024-04-01T00:00:00', endDate='2024-04-01T00:10:00', timeFormat='iso')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=2280)
        self.validate_response_field_timestamp(response, 'timestamp', is_iso=True)

    # ==================================================================================================================

    def test_invalid_parameter(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', invalid='parameter')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER)

    def test_invalid_timestamp(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', startDate='<timestamp>')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER_TIMESTAMP)

    def test_unknown_exchange(self):
        response = self.call_endpoint(exchange='<exchange>', currency='BTC')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)

    def test_unknown_currency(self):
        response = self.call_endpoint(exchange='deribit', currency='<currency>')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)


# ======================================================================================================================

if __name__ == '__main__':
    unittest.main()

# ======================================================================================================================
