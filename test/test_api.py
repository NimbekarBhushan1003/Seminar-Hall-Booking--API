import sys
import os

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
import json
from controller.controller import app


class TestSeminarHallBookingAPI(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_get_all_bookings(self):
        response = self.client.get('/assignment/bookings')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertIn("response", data)
        self.assertEqual(data["status"], "success")

    def test_book_best_fit_hall(self):
        payload = {
            "capacity": 120,
            "startTime": "2025-12-27 15:00:00",
            "endTime": "2025-12-27 16:00:00"
        }

        response = self.client.post(
            '/book',
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["status"], "success")
        self.assertIn("bookedHall", data["response"])

    def test_book_invalid_json(self):
        response = self.client.post(
            '/book',
            data=json.dumps({}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)

    def test_book_capacity_exceed(self):
        payload = {
            "capacity": 1500,
            "startTime": "2025-12-27 15:00:00",
            "endTime": "2025-12-27 16:00:00"
        }

        response = self.client.post(
            '/book',
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
