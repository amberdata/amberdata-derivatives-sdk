# ======================================================================================================================

# pylint: disable=line-too-long, missing-class-docstring, missing-function-docstring, missing-module-docstring, too-many-public-methods

import unittest

from tests.base_test_case import BaseTestCase
from tests.error_message import ErrorMessage


# ======================================================================================================================

class EndpointTradesFlowVolumeAggregatesTestCase(BaseTestCase):
    # pylint: disable-next=arguments-differ
    def setUp(self):
        super().setUp(
            function_name='get_trades_flow_volume_aggregates',
            imprecise_fields=[
                'payload.data[*].contractVolumeBlocked',
                'payload.data[*].contractVolumeOnScreen',
                'payload.data[*].notionalVolumeBlocked',
                'payload.data[*].notionalVolumeOnScreen',
                'payload.data[*].premiumVolumeBlocked',
                'payload.data[*].premiumVolumeOnScreen',
            ],
            precision_error=0.01
        )

    # ==================================================================================================================

    # TODO: API returns no records
    def test_default(self):
        response = self.call_endpoint(currency='MSTR')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=300)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field_timestamp(response, 'timestamp', is_milliseconds=True)

    def test_historical(self):
        response = self.call_endpoint(currency='MSTR', startDate='2024-11-29T15:00:00', endDate='2024-11-29T16:00:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=60)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field_timestamp(response, 'timestamp', is_milliseconds=True)

    def test_historical_timeformat_default(self):
        response = self.call_endpoint(currency='MSTR', startDate='2024-11-29T15:00:00', endDate='2024-11-29T16:00:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=60)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field_timestamp(response, 'timestamp', is_milliseconds=True)

    def test_historical_timeformat_hr(self):
        response = self.call_endpoint(currency='MSTR', startDate='2024-11-29T15:00:00', endDate='2024-11-29T16:00:00', timeFormat='hr')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=60)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field_timestamp(response, 'timestamp', is_hr=True, is_minutely=True)

    def test_historical_timeformat_iso(self):
        response = self.call_endpoint(currency='MSTR', startDate='2024-11-29T15:00:00', endDate='2024-11-29T16:00:00', timeFormat='iso')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=60)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field_timestamp(response, 'timestamp', is_iso=True, is_minutely=True)

    def test_historical_timeinterval_days(self):
        response = self.call_endpoint(currency='MSTR', startDate='2024-11-29T15:00:00', endDate='2024-11-29T16:00:00', timeFormat='hr', timeInterval='d')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=1)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field_timestamp(response, 'timestamp', is_hr=True, is_daily=True)

    def test_historical_timeinterval_hours(self):
        response = self.call_endpoint(currency='MSTR', startDate='2024-11-29T15:00:00', endDate='2024-11-29T16:00:00', timeFormat='hr', timeInterval='h')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=2)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field_timestamp(response, 'timestamp', is_hr=True, is_hourly=True)

    def test_historical_timeinterval_minutes(self):
        response = self.call_endpoint(currency='MSTR', startDate='2024-11-29T15:00:00', endDate='2024-11-29T16:00:00', timeFormat='hr', timeInterval='m')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=60)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field_timestamp(response, 'timestamp', is_hr=True, is_minutely=True)

    def test_historical_timeinterval_weeks(self):
        response = self.call_endpoint(currency='MSTR', startDate='2024-11-29T15:00:00', endDate='2024-11-29T16:00:00', timeFormat='hr', timeInterval='w')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=1)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field_timestamp(response, 'timestamp', is_hr=True, is_weekly=True)

    def test_historical_timeinterval_years(self):
        response = self.call_endpoint(currency='MSTR', startDate='2024-11-29T15:00:00', endDate='2024-11-29T16:00:00', timeFormat='hr', timeInterval='y')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=1)
        self.validate_response_field(response, 'exchange', 'tradfi')
        self.validate_response_field(response, 'currency', 'MSTR')
        self.validate_response_field_timestamp(response, 'timestamp', is_hr=True, is_yearly=True)

    # ==================================================================================================================

    def test_invalid_parameter(self):
        response = self.call_endpoint(currency='MSTR', invalid='parameter')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER)

    def test_invalid_exchange(self):
        response = self.call_endpoint(exchange='<exchange>', currency='BTC')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.UNSUPPORTED_EXCHANGE)

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
