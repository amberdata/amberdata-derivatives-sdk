# ======================================================================================================================

"""
Module to handle all the uni tests common functionalities and helper functions.
"""

# ======================================================================================================================

import inspect
import json
import os
import pathlib
import unittest

import copy
import dotenv
import jsonpath_ng as jp
import jsonschema

from amberdata_derivatives import AmberdataDerivatives

dotenv.load_dotenv()


# ======================================================================================================================

class BaseTestCase(unittest.TestCase):
    """
    Class to handle all the uni tests common functionalities and helper functions.
    """

    def setUp(
            self,
            function_name: str = None,
            time_format: str = None,
            ignore_fields: list = None,
            imprecise_fields: list = None,
            precision_error: float = 0.000001
    ):
        self.record_api_calls = os.getenv('RECORD_API_CALLS', 'false') == 'true'
        self.amberdata_client = AmberdataDerivatives(api_key=os.getenv('API_KEY'), time_format=time_format)
        self.function_name = function_name
        self.fixtures_directory = 'tests/fixtures'
        self.schemata_directory = 'tests/schemata'
        self.schema = self.__load_schema()
        self.ignore_fields = ignore_fields
        self.imprecise_fields = imprecise_fields
        self.precision_error = precision_error

        pathlib.Path(self.fixtures_directory).mkdir(parents=True, exist_ok=True)
        pathlib.Path(self.schemata_directory).mkdir(parents=True, exist_ok=True)

    # ==================================================================================================================

    def call_endpoint(self, **kwargs):
        """
        Calls the function on the amberdata_client as specified by the function name passed in the constructor.

        :param kwargs:  Arguments to pass to the function call
        """
        return getattr(self.amberdata_client, self.function_name)(**kwargs)

    # ==================================================================================================================

    def validate_response_data(self, response, file=None):
        """
        Validates that the response payload matches the expected fixture.

        :param response:  The response payload
        :param file:      The file from which to load the fixture - or the name of the calling function if not specified
        """
        self.__record_response_data(response)

        # Load fixture
        file = self.__ensure_fixture_file(self.fixtures_directory, inspect.stack()[1].function, file)
        with open(file, 'r', encoding='utf-8') as f:
            expected = json.load(f)

        # Remove fields to ignore if any
        actual = copy.deepcopy(response)
        if self.ignore_fields is not None:
            for field in self.ignore_fields:
                query = jp.parse(field)
                query.filter(lambda d: True, expected)
                query.filter(lambda d: True, actual)

        # Useful for debugging
        # with open('expected.json', 'w', encoding='utf-8') as f:
        #     json.dump(expected, f, indent=2, sort_keys=True)
        # with open('actual.json', 'w', encoding='utf-8') as f:
        #     json.dump(actual, f, indent=2, sort_keys=True)

        # Validate & remove imprecise fields if any
        if self.imprecise_fields is not None:
            for field in self.imprecise_fields:
                query = jp.parse(field)

                # Extract & validate field values
                expected_values = [match.value for match in query.find(expected)]
                actual_values = [match.value for match in query.find(actual)]

                self.assertEqual(len(expected_values), len(actual_values))
                for index, expected_value in enumerate(expected_values):
                    if expected_value is not None and actual_values[index] is not None:
                        self.assertLessEqual(abs(expected_value - actual_values[index]), self.precision_error)

                # Remove imprecise fields
                query.filter(lambda d: True, expected)
                query.filter(lambda d: True, actual)

        # Special clean-up
        self.__clean_error_message(actual)

        # Check data
        self.assertEqual(expected, actual)

    def validate_response_schema(self, response, file=None, schema=None):
        """
        Validates that the response payload follows the expected schema.

        :param response:  The response payload
        :param file:      The file from which to load the schema (only of schema is not specified)
        :param schema:    The schema against which to validate the response
        """
        if schema is None:
            file = self.__ensure_fixture_file(self.schemata_directory, inspect.stack()[1].function, file)

            with open(file, 'r', encoding='utf-8') as f:
                schema = json.load(f)

        jsonschema.validate(response, schema)

    def validate_response_200(self, response, num_elements=None, min_elements=None, max_elements=None):
        """
        Validates that the response payload succeeded with a 200 (Success).

        :param response:      The response payload
        :param num_elements:  If specified, the response should have exactly  this number of elements
        :param min_elements:  If specified, the response should have at least this number of elements
        :param max_elements:  If specified, the response should have at most  this number of elements
        """
        payload = response['payload']

        self.assertEqual('Successful request', response['description'])
        self.assertEqual(200,                  response['status'])
        self.assertEqual('OK',                 response['title'])
        self.assertEqual('2023-09-30',         payload['metadata']['api-version'])

        if num_elements is not None:
            self.assertEqual(len(payload['data']), num_elements)

        if min_elements is not None:
            self.assertGreaterEqual(len(payload['data']), min_elements)

        if max_elements is not None:
            self.assertLessEqual(len(payload['data']), max_elements)

    def validate_response_400(self, response, message: str):
        """
        Validates that the response payload is a 404 (Not Found).

        :param response:  The response payload
        :param message:   The message associated with the response
        """
        description = 'Request was invalid or cannot be served. See message for details'

        # Special clean-up
        self.__clean_error_message(response)

        self.assertEqual(description,   response['description'])
        self.assertEqual(400,           response['status'])
        self.assertEqual('BAD REQUEST', response['title'])
        self.assertEqual(True,          response['error'])
        self.assertEqual(message,       response['message'])

    def validate_response_field(self, response, field_name: str, field_value, field_value2=None):
        """
        Validates that the field with name `field_name` has the value `field_value`.

        :param response:      The response payload
        :param field_name:    The name of the field to validate
        :param field_value:   The value expected for the field (either/or)
        :param field_value2:  The value expected for the field (either/or)
        """
        data = response['payload']['data']

        if field_value2 is None:
            for element in data:
                self.assertEqual(element[field_name], field_value)
        else:
            for element in data:
                self.assertTrue(element[field_name] == field_value or element[field_name] == field_value2)

    def validate_response_field_timestamp(
        self,
        response,
        field_name: str,
        is_hr=False,
        is_iso=False,
        is_milliseconds=False,
        is_minutely=False,
        is_hourly=False,
        is_daily=False,
        is_weekly=False,
        is_yearly=False,
        is_nullable=False,
        is_zeroable=False
    ):
        """
        Validates a timestamp field in the response payload.

        :param response:         The response payload
        :param field_name:       The name of the field to validate
        :param is_hr:            The timestamp field should be written in Human Readable format
        :param is_iso:           The timestamp field should be written in ISO format
        :param is_milliseconds:  The timestamp field should be written in Milliseconds format
        :param is_minutely:      The timestamp field is expressed in minutes (no seconds)
        :param is_hourly:        The timestamp field is expressed in hours (seconds=minutes=00)
        :param is_daily:         The timestamp field is expressed in days (seconds=minutes=hours=00)
        :param is_weekly:        The timestamp field is expressed in weeks (seconds=minutes=hours=00)
        :param is_yearly:        The timestamp field is expressed in years (seconds=minutes=hours=days=months=00)
        :param is_nullable:      The timestamp field could be null
        :param is_zeroable:      The timestamp field could be zero
        """
        data = response['payload']['data']

        # Match timestamps with format: 2024-04-01 02:59:00 000
        if is_hr:
            regex = r'^[1-2][0-9]{3}-[0-1][0-9]-[0-3][0-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9] [0-9]{3}$'
            regex = r'^[1-2][0-9]{3}-[0-1][0-9]-[0-3][0-9] [0-2][0-9]:[0-5][0-9]:00 000$' if is_minutely else regex
            regex = r'^[1-2][0-9]{3}-[0-1][0-9]-[0-3][0-9] [0-2][0-9]:00:00 000$' if is_hourly else regex
            regex = r'^[1-2][0-9]{3}-[0-1][0-9]-[0-3][0-9] 00:00:00 000$' if is_daily else regex
            regex = r'^[1-2][0-9]{3}-[0-1][0-9]-[0-3][0-9] 00:00:00 000$' if is_weekly else regex  # TODO: improve
            regex = r'^[1-2][0-9]{3}-01-01 00:00:00 000$' if is_yearly else regex

            for element in data:
                self.assertRegex(element[field_name], regex)

        # Match timestamps with format: 2024-04-01T02:59:00.000Z
        if is_iso:
            regex = r'^[1-2][0-9]{3}-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9]\.[0-9]{3}Z$'
            regex = r'^[1-2][0-9]{3}-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:00\.000Z$' if is_minutely else regex
            regex = r'^[1-2][0-9]{3}-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:00:00\.000Z$' if is_hourly else regex
            regex = r'^[1-2][0-9]{3}-[0-1][0-9]-[0-3][0-9]T00:00:00\.000Z$' if is_daily else regex
            regex = r'^[1-2][0-9]{3}-[0-1][0-9]-[0-3][0-9]T00:00:00\.000Z$' if is_weekly else regex  # TODO: improve
            regex = r'^[1-2][0-9]{3}-01-01T00:00:00\.000Z$' if is_yearly else regex

            for element in data:
                self.assertRegex(element[field_name], regex)

        # Match timestamps expressed as milliseconds
        if is_milliseconds:
            for element in data:
                # Slow implementation requiring a conversion from int to string.
                # Milliseconds start with 1, followed by 12 digits
                # self.assertRegex(str(element[field_name]), r'^1[0-9]{12}$')

                # Better implementation comparing numbers.
                # 1293840000000 = 2011-01-01 00:00:00
                # 1893456000000 = 2030-01-01 00:00:00
                if element[field_name] == 0:
                    if not is_zeroable:
                        raise AssertionError(f'Timestamp field \'{field_name}\' in record is zero ({element}).')
                elif element[field_name] is None:
                    if not is_nullable:
                        raise AssertionError(f'Timestamp field \'{field_name}\' in record is null ({element}).')
                else:
                    self.__assert_between(element[field_name], 1293840000000, 1893456000000)
                    # pylint: disable=multiple-statements
                    if is_minutely: self.assertTrue(element[field_name] % 60000 == 0)
                    if is_hourly: self.assertTrue(element[field_name] % 3600000 == 0)
                    if is_daily: self.assertTrue(element[field_name] % 86400000 == 0)
                    if is_weekly: self.assertTrue(element[field_name] % 604800000 == 0)
                    # pylint: enable=multiple-statements

    # ==================================================================================================================

    def __load_schema(self, filename: str = None):
        if filename is None:
            filename = 'endpoint.' + self.function_name + '.json'

        with open(self.schemata_directory + '/' + filename, 'r', encoding='utf-8') as f:
            schema = json.load(f)

        return schema

    def __ensure_fixture_file(self, directory: str, filename: str, file):
        if file is None:
            path = directory + '/' + type(self).__name__
            pathlib.Path(path).mkdir(parents=True, exist_ok=True)
            file = path + '/' + filename + '.json'
        return file

    @staticmethod
    def __assert_between(x, low, high):
        # Naive implementation
        # self.assertGreaterEqual(x, low)
        # self.assertLessEqual(x, high)

        # Implementation requiring only one call/comparison
        if not isinstance(x, int):
            raise AssertionError(f'{x} is not an integer')

        if not low <= x <= high:
            raise AssertionError(f'{x} not between {low} and {high}')

    def __record_response_data(self, response, file=None):
        if not self.record_api_calls:
            return

        file = self.__ensure_fixture_file(self.fixtures_directory, inspect.stack()[2].function, file)

        with open(file, 'w', encoding='utf-8') as f:
            json.dump(response, f, indent=2, sort_keys=True)

    @staticmethod
    def __clean_error_message(response):
        # Special case to handle incompatibilities between two different versions of the API
        # TODO: remove this function once the migration is over
        if 'message' in response:
            response['message'] = response['message'].replace(
                '[ALL,P,p,put,Put,PUT,C,c,call,Call,CALL]',
                '[P,p,put,Put,PUT,C,c,call,Call,CALL]'
            )
        return response


# ======================================================================================================================
