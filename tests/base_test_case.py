# ======================================================================================================================

from amberdata_derivatives import AmberdataDerivatives
import inspect
import json
import jsonschema
from dotenv import load_dotenv
import os
import pathlib
import unittest

load_dotenv()


# ======================================================================================================================

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.record_api_calls = os.getenv("RECORD_API_CALLS", "false") == "true"
        self.amberdata_client = AmberdataDerivatives(api_key=os.getenv("API_KEY"))
        self.fixtures_directory = "tests/fixtures"
        self.schemata_directory = "tests/schemata"
        pathlib.Path(self.fixtures_directory).mkdir(parents=True, exist_ok=True)
        pathlib.Path(self.schemata_directory).mkdir(parents=True, exist_ok=True)

    def load_schema(self, filename: str):
        with open(self.schemata_directory + "/" + filename, 'r') as f:
            schema = json.load(f)
        return schema

    def validate_response_data(self, response, file=None):
        self.__record_response_data(response)

        file = self.__ensure_fixture_file(self.fixtures_directory, inspect.stack()[1].function, file)

        with open(file, 'r') as f:
            expected = json.load(f)

        self.assertEqual(expected, response)

    def validate_response_schema(self, response, file=None, schema=None):
        if schema is None:
            file = self.__ensure_fixture_file(self.schemata_directory, inspect.stack()[1].function, file)

            with open(file, 'r') as f:
                schema = json.load(f)

        jsonschema.validate(response, schema)

    def validate_response_200(self, response, num_elements=None, min_elements=None, max_elements=None):
        payload = response['payload']

        self.assertEqual("Successful request", response['description'])
        self.assertEqual(200,                  response['status'])
        self.assertEqual("OK",                 response['title'])
        self.assertEqual("2023-09-30",         payload['metadata']['api-version'])

        if num_elements is not None:
            self.assertEqual(len(payload['data']), num_elements)

        if min_elements is not None:
            self.assertGreaterEqual(len(payload['data']), min_elements)

        if max_elements is not None:
            self.assertLessEqual(len(payload['data']), max_elements)

    def validate_response_400(self, response, message: str):
        description = "Request was invalid or cannot be served. See message for details"

        self.assertEqual(description,   response['description'])
        self.assertEqual(400,           response['status'])
        self.assertEqual("BAD REQUEST", response['title'])
        self.assertEqual(True,          response['error'])
        self.assertEqual(message,       response['message'])

    def validate_response_field(self, response, field_name: str, field_value):
        data = response['payload']['data']

        for element in data:
            self.assertEqual(element[field_name], field_value)

    def validate_response_field_timestamp(self, response, field_name: str, isHr=False, isIso=False, isMilliseconds=False, isMinutely=False, isHourly=False, isDaily=False):
        data = response['payload']['data']

        # Match timestamps with format: 2024-04-01 02:59:00 000
        if isHr:
            regex = r'^[1-2][0-9]{3}-[0-1][0-9]-[0-3][0-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9] [0-9]{3}$'
            regex = r'^[1-2][0-9]{3}-[0-1][0-9]-[0-3][0-9] [0-2][0-9]:[0-5][0-9]:00 000$' if isMinutely else regex
            regex = r'^[1-2][0-9]{3}-[0-1][0-9]-[0-3][0-9] [0-2][0-9]:00:00 000$' if isHourly else regex
            regex = r'^[1-2][0-9]{3}-[0-1][0-9]-[0-3][0-9] 00:00:00 000$' if isDaily else regex

            for element in data:
                self.assertRegex(element[field_name], regex)

        # Match timestamps with format: 2024-04-01T02:59:00.000Z
        if isIso:
            regex = r'^[1-2][0-9]{3}-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9]\.[0-9]{3}Z$'
            regex = r'^[1-2][0-9]{3}-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:00\.000Z$' if isMinutely else regex
            regex = r'^[1-2][0-9]{3}-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:00:00\.000Z$' if isHourly else regex
            regex = r'^[1-2][0-9]{3}-[0-1][0-9]-[0-3][0-9]T00:00:00\.000Z$' if isDaily else regex

            for element in data:
                self.assertRegex(element[field_name], regex)

        # Match timestamps expressed as milliseconds
        if isMilliseconds:
            for element in data:
                # Slow implementation requiring a conversion from int to string.
                # Milliseconds start with 1, followed by 12 digits
                # self.assertRegex(str(element[field_name]), r'^1[0-9]{12}$')

                # Better implementation comparing numbers.
                # 1293840000000 = 2011-01-01 00:00:00
                # 1893456000000 = 2030-01-01 00:00:00
                self.__assert_between(element[field_name], 1293840000000, 1893456000000)

    # ==================================================================================================================

    def __ensure_fixture_file(self, directory: str, filename: str, file):
        if file is None:
            path = directory + "/" + type(self).__name__
            pathlib.Path(path).mkdir(parents=True, exist_ok=True)
            file = path + "/" + filename + ".json"
        return file

    @staticmethod
    def __assert_between(x, low, high):
        # Naive implementation
        # self.assertGreaterEqual(x, low)
        # self.assertLessEqual(x, high)

        # Implementation requiring only one call/comparison
        if not isinstance(x, int):
            raise AssertionError('%r is not an integer' % x)

        if not (low <= x <= high):
            raise AssertionError('%r not between %r and %r' % (x, low, high))

    def __record_response_data(self, response, file=None):
        if not self.record_api_calls:
            return

        file = self.__ensure_fixture_file(self.fixtures_directory, inspect.stack()[2].function, file)

        with open(file, 'w') as f:
            json.dump(response, f, indent=2, sort_keys=True)

# ======================================================================================================================
