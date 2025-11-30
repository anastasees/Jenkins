import unittest
from lab_4 import app, meter_service

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        meter_service.meters = {}

    def test_home_status_code(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_add_meter(self):
        response = self.app.post('/add', data={'meter_id': '999', 'status': 'New'})
        self.assertEqual(response.status_code, 302)
        self.assertIn('999', meter_service.meters)

if __name__ == '__main__':
    unittest.main()