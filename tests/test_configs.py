from .base import *


class TestDevelopmentConfig(BaseTestCase):
    def setUp(self):
        super(TestDevelopmentConfig, self).setUp()
        self.app = create_app('development')

    def test_app_is_development(self):
        self.assertFalse(current_app is None)
        self.assertTrue(self.app.config['DEBUG'] is True)
        self.assertTrue(self.app.config['TESTING'] is False)


class TestTestingConfig(BaseTestCase):
    def setUp(self):
        super(TestTestingConfig, self).setUp()
        self.app = create_app('testing')

    def test_app_is_testing(self):
        self.assertFalse(current_app is None)
        self.assertTrue(self.app.config['DEBUG'] is True)
        self.assertTrue(self.app.config['TESTING'] is True)


class TestProductionConfig(BaseTestCase):
    def setUp(self):
        super(TestProductionConfig, self).setUp()
        self.app = create_app('production')

    def test_app_is_production(self):
        self.assertFalse(current_app is None)
        self.assertTrue(self.app.config['DEBUG'] is False)
        self.assertTrue(self.app.config['TESTING'] is False)


if __name__ == "__main__":
    unittest.main()
