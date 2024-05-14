# ======================================================================================================================

from .base_test_case import BaseTestCase
import unittest


# ======================================================================================================================

class EndpointDeltaSurfaceFloatingTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.schema = self.load_schema('endpoint.delta_surface_floating.json')

    # ==================================================================================================================

    def test_default(self):
        response = self.amberdata_client.get_delta_surfaces_floating(exchange='deribit', currency='BTC')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=10)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'timestamp', isIso=True) # TODO: this should be 'isMilliseconds=True'

    def test_timestamp(self):
        response = self.amberdata_client.get_delta_surfaces_floating(exchange='deribit', currency='BTC', startDate='2024-04-01T00:00:00', endDate='2024-04-02T00:00:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=14400)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'timestamp', isIso=True) # TODO: this should be 'isMilliseconds=True'

    def test_timestamp_timeFormat_hr(self):
        response = self.amberdata_client.get_delta_surfaces_floating(exchange='deribit', currency='BTC', startDate='2024-04-01T00:00:00', endDate='2024-04-02T00:00:00', timeFormat='hr')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=14400)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'timestamp', isHr=True, isMinutely=True)

    def test_timestamp_timeFormat_iso(self):
        response = self.amberdata_client.get_delta_surfaces_floating(exchange='deribit', currency='BTC', startDate='2024-04-01T00:00:00', endDate='2024-04-02T00:00:00', timeFormat='iso')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=14400)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'timestamp', isIso=True, isMinutely=True)

    def test_timestamp_timeInterval_days(self):
        response = self.amberdata_client.get_delta_surfaces_floating(exchange='deribit', currency='BTC', startDate='2024-04-01T00:00:00', endDate='2024-04-02T00:00:00', timeFormat='hr', timeInterval='d')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=10)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'timestamp', isHr=True, isDaily=True)

    def test_timestamp_timeInterval_hours(self):
        response = self.amberdata_client.get_delta_surfaces_floating(exchange='deribit', currency='BTC', startDate='2024-04-01T00:00:00', endDate='2024-04-02T00:00:00', timeFormat='hr', timeInterval='h')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=240)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'timestamp', isHr=True, isHourly=True)

    def test_timestamp_timeInterval_minutes(self):
        response = self.amberdata_client.get_delta_surfaces_floating(exchange='deribit', currency='BTC', startDate='2024-04-01T00:00:00', endDate='2024-04-02T00:00:00', timeFormat='hr', timeInterval='m')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=14400)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'timestamp', isHr=True, isMinutely=True)

    # ==================================================================================================================

    def test_invalid_parameter(self):
        response = self.amberdata_client.get_delta_surfaces_floating(exchange='deribit', currency='BTC', invalid='parameter')
        self.validate_response_data(response)
        self.validate_response_400(response, "Parameter 'invalid' is not supported.")

    def test_invalid_timestamp(self):
        response = self.amberdata_client.get_delta_surfaces_floating(exchange='deribit', currency='BTC', startDate='<timestamp>')
        self.validate_response_data(response)
        self.validate_response_400(response, "Invalid timestamp value: '<timestamp>'.")

    def test_unknown_exchange(self):
        response = self.amberdata_client.get_delta_surfaces_floating(exchange='<exchange>', currency='BTC')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)

    def test_unknown_currency(self):
        response = self.amberdata_client.get_delta_surfaces_floating(exchange='deribit', currency='<currency>')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)


# ======================================================================================================================

if __name__ == '__main__':
    unittest.main()

# ======================================================================================================================
