# ======================================================================================================================

# pylint: disable=missing-class-docstring, missing-function-docstring, missing-module-docstring

import unittest

from amberdata_derivatives.version import __version__
from tests.base_test_case import BaseTestCase


# ======================================================================================================================

class EndpointVersionTestCase(BaseTestCase):
    def setUp(self, function_name='get_version'):
        super().setUp(function_name)

    # ==================================================================================================================

    def test_default(self):
        response = self.call_endpoint()
        self.validate_response_data(response)
        self.assertEqual(__version__, response)


# ======================================================================================================================

if __name__ == '__main__':
    unittest.main()

# ======================================================================================================================
