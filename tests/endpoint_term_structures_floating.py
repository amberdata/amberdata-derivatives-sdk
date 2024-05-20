# ======================================================================================================================

import unittest

from .base_test_case import BaseTestCase


# ======================================================================================================================

class EndpointTermStructureFloatingTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.schema = self.load_schema('endpoint.term_structures_floating.json')

    # ==================================================================================================================

    def test_default(self):
        response = self.amberdata_client.get_term_structures_floating(exchange='deribit', currency='BTC')
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=10)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'timestamp', is_iso=True) # TODO: this should be 'is_milliseconds=True'

    def test_timestamp(self):
        response = self.amberdata_client.get_term_structures_floating(exchange='deribit', currency='BTC', timestamp='2024-04-01T03:00:00')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=10)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'timestamp', is_iso=True) # TODO: this should be 'is_milliseconds=True'

    def test_timestamp_timeformat_hr(self):
        response = self.amberdata_client.get_term_structures_floating(exchange='deribit', currency='BTC', timestamp='2024-04-01T03:00:00', timeFormat='hr')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=10)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'timestamp', is_hr=True)

    def test_timestamp_timeformat_iso(self):
        response = self.amberdata_client.get_term_structures_floating(exchange='deribit', currency='BTC', timestamp='2024-04-01T03:00:00', timeFormat='iso')
        self.validate_response_data(response)
        self.validate_response_schema(response, schema=self.schema)
        self.validate_response_200(response, min_elements=10)
        self.validate_response_field(response, 'exchange', 'deribit')
        self.validate_response_field(response, 'currency', 'BTC')
        self.validate_response_field_timestamp(response, 'timestamp', is_iso=True)

    # ==================================================================================================================

    def test_invalid_parameter(self):
        response = self.amberdata_client.get_term_structures_floating(exchange='deribit', currency='BTC', invalid='parameter')
        self.validate_response_data(response)
        self.validate_response_400(response, "Parameter 'invalid' is not supported.")

    def test_invalid_timestamp(self):
        response = self.amberdata_client.get_term_structures_floating(exchange='deribit', currency='BTC', timestamp='<timestamp>')
        self.validate_response_data(response)
        self.validate_response_400(response, "Invalid timestamp value: '<timestamp>'.")

    def test_unknown_exchange(self):
        response = self.amberdata_client.get_term_structures_floating(exchange='<exchange>', currency='BTC')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)

    def test_unknown_currency(self):
        response = self.amberdata_client.get_term_structures_floating(exchange='deribit', currency='<currency>')
        self.validate_response_data(response)
        self.validate_response_200(response, num_elements=0)


# ======================================================================================================================

if __name__ == '__main__':
    unittest.main()

# ======================================================================================================================
