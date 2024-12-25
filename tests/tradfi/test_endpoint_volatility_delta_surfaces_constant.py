# ======================================================================================================================

# pylint: disable=line-too-long, missing-class-docstring, missing-function-docstring, missing-module-docstring

import unittest

from tests.base_test_case import BaseTestCase
from tests.error_message import ErrorMessage


# ======================================================================================================================

class EndpointVolatilityDeltaSurfaceConstantTestCase(BaseTestCase):
    # pylint: disable-next=arguments-differ
    def setUp(self):
        super().setUp(
            function_name='get_volatility_delta_surfaces_constant',
            imprecise_fields=['payload.data[*].openInterest']
        )

    # ==================================================================================================================

    # def test_default(self):
    #     response = self.call_endpoint(exchange='deribit', currency='BTC')
    #     self.validate_response_schema(response, schema=self.schema)
    #     self.validate_response_200(response, min_elements=10)
    #     self.validate_response_field(response, 'exchange', 'deribit')
    #     self.validate_response_field(response, 'currency', 'BTC')
    #     self.validate_response_field_timestamp(response, 'timestamp', is_iso=True) # TODO: this should be 'is_milliseconds=True'

    def test_historical_timeformat_default(self):
        response = self.call_endpoint(currency='MSTR', startDate='2024-12-20T00:00:00', endDate='2024-12-21T00:00:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=70)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field_timestamp(response, 'timestamp', is_milliseconds=True)

    def test_historical_timeformat_hr(self):
        response = self.call_endpoint(currency='MSTR', startDate='2024-12-20T00:00:00', endDate='2024-12-21T00:00:00', timeFormat='hr')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=70)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field_timestamp(response, 'timestamp', is_hr=True, is_minutely=True)

    def test_historical_timeformat_iso(self):
        response = self.call_endpoint(currency='MSTR', startDate='2024-12-20T00:00:00', endDate='2024-12-21T00:00:00', timeFormat='iso')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=70)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field_timestamp(response, 'timestamp', is_iso=True, is_minutely=True)

    def test_historical_timeinterval_days(self):
        response = self.call_endpoint(currency='MSTR', startDate='2024-12-19T00:00:00', endDate='2024-12-21T00:00:00', timeFormat='hr', timeInterval='d')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=10)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')

        data = response['payload']['data']
        for i, element in enumerate(data):
            for key in element:
                if type(element[key]) is str:
                    data[i][key] = element[key].replace('20:00:00', '00:00:00')

        self.validate_response_field_timestamp(response, 'timestamp', is_hr=True, is_daily=True)

    def test_historical_timeinterval_hours(self):
        response = self.call_endpoint(currency='MSTR', startDate='2024-12-20T00:00:00', endDate='2024-12-21T00:00:00', timeFormat='hr', timeInterval='h')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=10)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field_timestamp(response, 'timestamp', is_hr=True, is_hourly=True)

    def test_historical_timeinterval_minutes(self):
        response = self.call_endpoint(currency='MSTR', startDate='2024-12-20T00:00:00', endDate='2024-12-21T00:00:00', timeFormat='hr', timeInterval='m')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=70)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field_timestamp(response, 'timestamp', is_hr=True, is_minutely=True)

    # ==================================================================================================================

    # def test_invalid_parameter(self):
    #     response = self.call_endpoint(currency='MSTR', invalid='parameter')
    #     self.validate_response_data(response)
    #     self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER)
    #
    # def test_invalid_exchange(self):
    #     response = self.call_endpoint(exchange='<exchange>', currency='MSTR')
    #     self.validate_response_data(response)
    #     self.validate_response_400(response, ErrorMessage.UNSUPPORTED_EXCHANGE)
    #
    # def test_invalid_timestamp(self):
    #     response = self.call_endpoint(currency='MSTR', startDate='<timestamp>')
    #     self.validate_response_data(response)
    #     self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER_TIMESTAMP)
    #
    # def test_unknown_currency(self):
    #     response = self.call_endpoint(currency='<currency>')
    #     self.validate_response_data(response)
    #     self.validate_response_200(response, num_elements=0)


# ======================================================================================================================

if __name__ == '__main__':
    unittest.main()

# ======================================================================================================================
