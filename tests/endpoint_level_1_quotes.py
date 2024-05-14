# ======================================================================================================================

from .base_test_case import BaseTestCase
import unittest


# ======================================================================================================================

class EndpointLevel1QuotesTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.schema = self.load_schema('endpoint.level_1_quotes.json')

    # ==================================================================================================================

    def test_default(self):
        response = self.amberdata_client.get_level_1_quotes(exchange='deribit', currency='BTC')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=500)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'timestamp', isIso=True) # TODO: this should be 'isMilliseconds=True'

    def test_instrument_historical(self):
        response = self.amberdata_client.get_level_1_quotes(exchange='deribit', currency='BTC', instrument='BTC-26APR24-100000-C', startDate='2024-04-01T00:00:00', endDate='2024-04-01T00:10:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=10)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field(response, 'instrument', 'BTC-26APR24-100000-C')
        self.validate_response_field_timestamp(response, 'timestamp', isIso=True) # TODO: this should be 'isMilliseconds=True'

    def test_isAtm_historical(self):
        response = self.amberdata_client.get_level_1_quotes(exchange='deribit', currency='BTC', isAtm=True, startDate='2024-04-01T00:00:00', endDate='2024-04-01T00:10:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=240)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field(response, 'isAtm', True)
        self.validate_response_field_timestamp(response, 'timestamp', isIso=True) # TODO: this should be 'isMilliseconds=True'

    def test_isAtm_realtime(self):
        response = self.amberdata_client.get_level_1_quotes(exchange='deribit', currency='BTC', isAtm=False)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=200)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field(response, 'isAtm', False)
        self.validate_response_field_timestamp(response, 'timestamp', isIso=True) # TODO: this should be 'isMilliseconds=True'

    def test_putCall_historical(self):
        response = self.amberdata_client.get_level_1_quotes(exchange='deribit', currency='BTC', putCall='C', startDate='2024-04-01T00:00:00', endDate='2024-04-01T00:10:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=5320)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field(response, 'putCall', 'C')
        self.validate_response_field_timestamp(response, 'timestamp', isIso=True) # TODO: this should be 'isMilliseconds=True'

    def test_putCall_realtime(self):
        response = self.amberdata_client.get_level_1_quotes(exchange='deribit', currency='BTC', putCall='P')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=200)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field(response, 'putCall', 'P')
        self.validate_response_field_timestamp(response, 'timestamp', isIso=True) # TODO: this should be 'isMilliseconds=True'

    def test_strike_historical(self):
        response = self.amberdata_client.get_level_1_quotes(exchange='deribit', currency='BTC', strike=50000, startDate='2024-04-01T00:00:00', endDate='2024-04-01T00:10:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=160)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field(response, 'strike', 50000)
        self.validate_response_field_timestamp(response, 'timestamp', isIso=True) # TODO: this should be 'isMilliseconds=True'

    def test_strike_realtime(self):
        response = self.amberdata_client.get_level_1_quotes(exchange='deribit', currency='BTC', strike=50000)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=1)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field(response, 'strike', 50000)
        self.validate_response_field_timestamp(response, 'timestamp', isIso=True) # TODO: this should be 'isMilliseconds=True'

    def test_timestamp(self):
        response = self.amberdata_client.get_level_1_quotes(exchange='deribit', currency='BTC', startDate='2024-04-01T00:00:00', endDate='2024-04-01T00:10:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=10640)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'timestamp', isIso=True) # TODO: this should be 'isMilliseconds=True'

    def test_timestamp_timeFormat_hr(self):
        response = self.amberdata_client.get_level_1_quotes(exchange='deribit', currency='BTC', startDate='2024-04-01T00:00:00', endDate='2024-04-01T00:10:00', timeFormat='hr')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=10640)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'timestamp', isHr=True, isMinutely=True)

    def test_timestamp_timeFormat_iso(self):
        response = self.amberdata_client.get_level_1_quotes(exchange='deribit', currency='BTC', startDate='2024-04-01T00:00:00', endDate='2024-04-01T00:10:00', timeFormat='iso')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=10640)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'timestamp', isIso=True, isMinutely=True)

    def test_timestamp_timeInterval_days(self):
        response = self.amberdata_client.get_level_1_quotes(exchange='deribit', currency='BTC', startDate='2024-04-01T00:00:00', endDate='2024-04-01T00:10:00', timeFormat='hr', timeInterval='d')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=1064)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'timestamp', isHr=True, isDaily=True)

    def test_timestamp_timeInterval_hours(self):
        response = self.amberdata_client.get_level_1_quotes(exchange='deribit', currency='BTC', startDate='2024-04-01T00:00:00', endDate='2024-04-01T00:10:00', timeFormat='hr', timeInterval='h')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=1064)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'timestamp', isHr=True, isHourly=True)

    def test_timestamp_timeInterval_minutes(self):
        response = self.amberdata_client.get_level_1_quotes(exchange='deribit', currency='BTC', startDate='2024-04-01T00:00:00', endDate='2024-04-01T00:10:00', timeFormat='hr', timeInterval='m')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, num_elements=10640)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'timestamp', isHr=True, isMinutely=True)

    # ==================================================================================================================

    def test_invalid_parameter(self):
        response = self.amberdata_client.get_level_1_quotes(exchange='deribit', currency='BTC', invalid='parameter')
        self.validate_response_data(response)
        self.validate_response_400(response, "Parameter 'invalid' is not supported.")

    # TODO: This test should fail - validation is missing in data-api
    @unittest.skip("Missing validation")
    def test_invalid_isAtm(self):
        response = self.amberdata_client.get_level_1_quotes(exchange='deribit', currency='BTC', isAtm='<is_atm>')
        self.validate_response_data(response)
        self.validate_response_200(response, min_elements=200)

    # TODO: This test should fail - validation is missing in data-api
    def test_invalid_putCall(self):
        response = self.amberdata_client.get_level_1_quotes(exchange='deribit', currency='BTC', putCall='<put_call>')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)

    # TODO: This test should fail, and not return a 500 - validation is missing in data-api
    @unittest.skip("Missing validation")
    def test_invalid_strike(self):
        response = self.amberdata_client.get_level_1_quotes(exchange='deribit', currency='BTC', strike='<strike>')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)

    def test_invalid_timestamp(self):
        response = self.amberdata_client.get_level_1_quotes(exchange='deribit', currency='BTC', startDate='<timestamp>')
        self.validate_response_data(response)
        self.validate_response_400(response, "Invalid timestamp value: '<timestamp>'.")

    def test_unknown_exchange(self):
        response = self.amberdata_client.get_level_1_quotes(exchange='<exchange>', currency='BTC')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)

    def test_unknown_currency(self):
        response = self.amberdata_client.get_level_1_quotes(exchange='deribit', currency='<currency>')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)


# ======================================================================================================================

if __name__ == '__main__':
    unittest.main()

# ======================================================================================================================
