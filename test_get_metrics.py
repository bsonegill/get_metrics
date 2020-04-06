import unittest
from flask_testing import TestCase
from get_metrics import app

class BaseTestCase(TestCase):
    def create_app(self):
        return app

    def setUp(self):
        pass

    def tearDown(self):
        pass

class FlaskTestCase(BaseTestCase):
    def test_get_metrics(self):
        pass

if __name__ == '__main__':
    unittest.main()
