# ======================================================================================================================

# pylint: disable=line-too-long, missing-class-docstring, missing-function-docstring, missing-module-docstring, too-many-public-methods

from datetime import datetime, timedelta, timezone, UTC
import unittest

from tests.base_test_case import BaseTestCase
from tests.error_message import ErrorMessage


# ======================================================================================================================

class EndpointOptionsScannerStrikesBoughtSoldTestCase(BaseTestCase):
    # pylint: disable-next=arguments-differ
    def setUp(self):
        super().setUp(
            function_name='get_options_scanner_strikes_bought_sold',
            imprecise_fields=[
                'payload.data[*].indexPrice',
                'payload.data[*].netPremium',
                'payload.data[*].tradeAmount'
            ],
            precision_error=0.0001
        )

        # Retrieve last know decorated trades
        start_date = (datetime.now(UTC) - timedelta(hours=12)).isoformat()
        end_date = datetime.now(UTC).isoformat()
        response = self.amberdata_client.get_trades_flow_decorated_trades('deribit', 'BTC', startDate=start_date, endDate=end_date)

        # Find the greater expiration
        expirations = []
        data = response['payload']['data']
        for row in data:
            expirations.append(row['expirationTimestamp'])
        expiration = sorted(set(expirations))[-1]

        self.__expiration = datetime.fromtimestamp(expiration / 1000.0, tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%S')

    # ==================================================================================================================

    def test_default(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', expiration=self.__expiration)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=1)
        self.validate_response_field_timestamp(response, 'expirationTimestamp', is_milliseconds=True)
        self.validate_response_field_timestamp(response, 'snapshotTimestamp', is_milliseconds=True)

    def test_default_timeformat_hr(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', expiration=self.__expiration, timeFormat='hr')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=1)
        self.validate_response_field_timestamp(response, 'expirationTimestamp', is_hr=True)
        self.validate_response_field_timestamp(response, 'snapshotTimestamp', is_hr=True)

    def test_default_timeformat_iso(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', expiration=self.__expiration, timeFormat='iso')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=1)
        self.validate_response_field_timestamp(response, 'expirationTimestamp', is_iso=True)
        self.validate_response_field_timestamp(response, 'snapshotTimestamp', is_iso=True)

    # ==================================================================================================================

    def test_invalid_parameter(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', expiration=self.__expiration, invalid='parameter')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER)

    def test_invalid_timestamp(self):
        response = self.call_endpoint(exchange='deribit', currency='BTC', expiration='<timestamp>')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.INVALID_PARAMETER_TIMESTAMP)

    def test_unknown_exchange(self):
        response = self.call_endpoint(exchange='<exchange>', currency='BTC', expiration=self.__expiration)
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)

    def test_unknown_currency(self):
        response = self.call_endpoint(exchange='deribit', currency='<currency>', expiration=self.__expiration)
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)


# ======================================================================================================================

if __name__ == '__main__':
    unittest.main()

# ======================================================================================================================
