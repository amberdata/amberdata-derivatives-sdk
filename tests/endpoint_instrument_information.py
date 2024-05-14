# ======================================================================================================================

from .base_test_case import BaseTestCase
import unittest


# ======================================================================================================================

class EndpointInstrumentTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.schema = self.load_schema('endpoint.instrument_information.json')

    # ==================================================================================================================

    def test_default(self):
        response = self.amberdata_client.get_instrument_information()
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=1500)
        self.validate_response_field_timestamp(response, 'endDate', isMilliseconds=True)
        self.validate_response_field_timestamp(response, 'expiration', isMilliseconds=True)

    def test_exchange(self):
        response = self.amberdata_client.get_instrument_information(exchange='deribit')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field_timestamp(response, 'endDate', isMilliseconds=True)
        self.validate_response_field_timestamp(response, 'expiration', isMilliseconds=True)

    def test_currency(self):
        response = self.amberdata_client.get_instrument_information(currency='ETH')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response)
        self.validate_response_field(response, 'currency', 'ETH')
        self.validate_response_field_timestamp(response, 'endDate', isMilliseconds=True)
        self.validate_response_field_timestamp(response, 'expiration', isMilliseconds=True)

    def test_putCall(self):
        response = self.amberdata_client.get_instrument_information(putCall='P')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response)
        self.validate_response_field(response, 'putCall', 'P')
        self.validate_response_field_timestamp(response, 'endDate', isMilliseconds=True)
        self.validate_response_field_timestamp(response, 'expiration', isMilliseconds=True)

    def test_strike(self):
        response = self.amberdata_client.get_instrument_information(strike=5000)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response)
        self.validate_response_field(response, 'strike', 5000)
        self.validate_response_field_timestamp(response, 'endDate', isMilliseconds=True)
        self.validate_response_field_timestamp(response, 'expiration', isMilliseconds=True)

    def test_timestamp(self):
        response = self.amberdata_client.get_instrument_information(timestamp='2024-04-01T03:00:00')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=2952)
        self.validate_response_field_timestamp(response, 'endDate', isMilliseconds=True)
        self.validate_response_field_timestamp(response, 'expiration', isMilliseconds=True)

    def test_timestamp_timeFormat_hr(self):
        response = self.amberdata_client.get_instrument_information(timestamp='2024-04-01T03:00:00', timeFormat='hr')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=2952)
        self.validate_response_field_timestamp(response, 'endDate', isHr=True)
        self.validate_response_field_timestamp(response, 'expiration', isHr=True)

    def test_timestamp_timeFormat_iso(self):
        response = self.amberdata_client.get_instrument_information(timestamp='2024-04-01T03:00:00', timeFormat='iso')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=2952)
        self.validate_response_field_timestamp(response, 'endDate', isIso=True)
        self.validate_response_field_timestamp(response, 'expiration', isIso=True)

    # ==================================================================================================================

    def test_invalid_parameter(self):
        response = self.amberdata_client.get_instrument_information(invalid='parameter')
        self.validate_response_data(response)
        self.validate_response_400(response, "Parameter 'invalid' is not supported.")

    def test_invalid_putCall(self):
        response = self.amberdata_client.get_instrument_information(putCall='<putcall>')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)

    # TODO: This test should fail, and not return a 500 - validation is missing in data-api
    @unittest.skip("Missing validation")
    def test_invalid_strike(self):
        response = self.amberdata_client.get_instrument_information(strike='<strike>')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)

    def test_invalid_timestamp(self):
        response = self.amberdata_client.get_instrument_information(timestamp='<timestamp>')
        self.validate_response_data(response)
        self.validate_response_400(response, "Invalid timestamp value: '<timestamp>'.")

    def test_invalid_timeFormat(self):
        response = self.amberdata_client.get_instrument_information(timeFormat='<time_format>')
        self.validate_response_data(response)
        self.validate_response_400(response, "Invalid argument timeFormat: expected one of [nanoseconds,ns,milliseconds,ms,iso,iso8601,iso8611,human,human_readable,humanReadable,hr], found '<time_format>'.")

    def test_unknown_currency(self):
        response = self.amberdata_client.get_instrument_information(currency='<currency>')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)

    def test_unknown_exchange(self):
        response = self.amberdata_client.get_instrument_information(exchange='<exchange>')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)


# ======================================================================================================================

if __name__ == '__main__':
    unittest.main()

# ======================================================================================================================
