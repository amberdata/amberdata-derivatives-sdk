# ======================================================================================================================

# pylint: disable=line-too-long, missing-class-docstring, missing-function-docstring, missing-module-docstring, too-many-public-methods

import datetime
import unittest

from tests.base_test_case import BaseTestCase
from tests.error_message import ErrorMessage


# ======================================================================================================================

class EndpointVolatilitySVIAltcoinsTestCase(BaseTestCase):
    # pylint: disable-next=arguments-differ
    def setUp(self):
        super().setUp(function_name='get_volatility_svi_altcoins')

    # ==================================================================================================================

    @staticmethod
    def _create_dates():
        end_date   = datetime.datetime.now(datetime.timezone.utc).date()
        start_date = end_date - datetime.timedelta(days=7)
        return [start_date, end_date]

    def _check_response(self, response):
        self.validate_response_200      (response, num_elements=2)
        self.validate_response_schema   (response, schema=self.schema)
        self.validate_response_field    (response, 'currency',          'BTC')
        self.validate_response_field_not(response, 'forwardDifference', None, '')
        self.validate_response_field_not(response, 'indexPrice',        None, '')
        self.validate_response_field_not(response, 'sviA',              None, '')
        self.validate_response_field_not(response, 'sviB',              None, '')
        self.validate_response_field_not(response, 'sviM',              None, '')
        self.validate_response_field_not(response, 'sviRho',            None, '')
        self.validate_response_field_not(response, 'sviSigma',          None, '')
        self.validate_response_field_not(response, 'timestamp',         None, '')

# ==================================================================================================================

    def test_default(self):
        response = self.call_endpoint(currency='BTC')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=2)
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'timestamp', is_milliseconds=True)

    def test_historical(self):
        [start_date, end_date] = self._create_dates()
        response = self.call_endpoint(currency='BTC', startDate=start_date.isoformat(), endDate=end_date.isoformat())
        self._check_response(response)
        self.validate_response_field_timestamp(response, 'timestamp', is_milliseconds=True)

    def test_historical_signature_ecdsa(self):
        [start_date, end_date] = self._create_dates()
        response = self.call_endpoint(currency='BTC', startDate=start_date, endDate=end_date, signature='ECDSA')
        self._check_response(response)
        self.validate_response_field_timestamp(response, 'timestamp', is_milliseconds=True)

        signature = response['payload']['metadata']['signature']
        self.assertNotEqual('',   signature)
        self.assertNotEqual(None, signature)
        self.assertTrue(signature.startswith('0x'))
        self.assertEqual(132, len(signature))

    def test_historical_sviformat_dte(self):
        [start_date, end_date] = self._create_dates()
        response = self.call_endpoint(currency='BTC', startDate=start_date, endDate=end_date, sviFormat='DTE')
        self._check_response(response)
        self.validate_response_field_timestamp(response, 'timestamp', is_milliseconds=True)

    def test_historical_sviformat_tau(self):
        [start_date, end_date] = self._create_dates()
        response = self.call_endpoint(currency='BTC', startDate=start_date, endDate=end_date, sviFormat='DTE')
        self._check_response(response)
        self.validate_response_field_timestamp(response, 'timestamp', is_milliseconds=True)

    def test_historical_timeformat_default(self):
        [start_date, end_date] = self._create_dates()
        response = self.call_endpoint(currency='BTC', startDate=start_date, endDate=end_date)
        self._check_response(response)
        self.validate_response_field_timestamp(response, 'timestamp', is_milliseconds=True)

    def test_historical_timeformat_hr(self):
        [start_date, end_date] = self._create_dates()
        response = self.call_endpoint(currency='BTC', startDate=start_date, endDate=end_date, timeFormat='hr')
        self._check_response(response)
        self.validate_response_field_timestamp(response, 'timestamp', is_hr=True, is_minutely=True)

    def test_historical_timeformat_iso(self):
        [start_date, end_date] = self._create_dates()
        response = self.call_endpoint(currency='BTC', startDate=start_date, endDate=end_date, timeFormat='iso')
        self._check_response(response)
        self.validate_response_field_timestamp(response, 'timestamp', is_iso=True, is_minutely=True)

    # ==================================================================================================================

    def test_invalid_parameter(self):
        response = self.call_endpoint(currency='BTC', invalid='parameter')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.UNSUPPORTED_PARAMETER_INVALID)

    def test_invalid_exchange(self):
        response = self.call_endpoint(exchange='<exchange>', currency='BTC')
        self.validate_response_data(response)
        self.validate_response_400(response, ErrorMessage.UNSUPPORTED_PARAMETER_EXCHANGE)

    def test_invalid_timestamp(self):
        response = self.call_endpoint(currency='BTC', startDate='<timestamp>')
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
