# test.py

import werkzeug
# Workaround for AttributeError: set a dummy __version__ if it does not exist.
if not hasattr(werkzeug, '__version__'):
    werkzeug.__version__ = '3.0.0'

import unittest
import json
from app import app

class StravaLiteAPITestCase(unittest.TestCase):
    def setUp(self):
        # Set up the Flask test client.
        self.app = app.test_client()
        self.app.testing = True

    def test_register_user(self):
        # Test user registration.
        response = self.app.post('/user', data=json.dumps({
            "name": "Test User",
            "age": 30
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("id", data)
        self.assertEqual(data["name"], "Test User")
        self.assertEqual(data["age"], 30)

    def test_get_nonexistent_user(self):
        # Retrieving a user that doesn't exist should yield a 404.
        response = self.app.get('/user/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_add_workout(self):
        # Register a new user.
        response = self.app.post('/user', data=json.dumps({
            "name": "Workout Tester",
            "age": 25
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        user_id = data["id"]

        # Add a workout for the user.
        workout_payload = {
            "date": "2025-04-15",
            "time": "30:00",
            "distance": "5km"
        }
        response = self.app.put(f'/workouts/{user_id}', data=json.dumps(workout_payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        workout_data = json.loads(response.data)
        self.assertEqual(workout_data["date"], "2025-04-15")
        self.assertEqual(workout_data["time"], "30:00")
        self.assertEqual(workout_data["distance"], "5km")

    def test_follow_and_show_friend_workouts(self):
        # Create two users.
        response1 = self.app.post('/user', data=json.dumps({
            "name": "User One",
            "age": 30
        }), content_type='application/json')
        self.assertEqual(response1.status_code, 200)
        user1 = json.loads(response1.data)
        user1_id = user1["id"]

        response2 = self.app.post('/user', data=json.dumps({
            "name": "User Two",
            "age": 35
        }), content_type='application/json')
        self.assertEqual(response2.status_code, 200)
        user2 = json.loads(response2.data)
        user2_id = user2["id"]

        # User Two adds a workout.
        workout_payload = {
            "date": "2025-04-16",
            "time": "45:00",
            "distance": "10km"
        }
        response = self.app.put(f'/workouts/{user2_id}', data=json.dumps(workout_payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # User One follows User Two.
        follow_payload = {"follow_id": user2_id}
        response = self.app.put(f'/follow-list/{user1_id}', data=json.dumps(follow_payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        follow_data = json.loads(response.data)
        self.assertIn(user2_id, follow_data["following"])

        # User One retrieves workouts for User Two.
        response = self.app.get(f'/follow-list/{user1_id}/{user2_id}')
        self.assertEqual(response.status_code, 200)
        friend_workouts_data = json.loads(response.data)
        self.assertIn("workouts", friend_workouts_data)
        self.assertEqual(len(friend_workouts_data["workouts"]), 1)

if __name__ == '__main__':
    unittest.main()
