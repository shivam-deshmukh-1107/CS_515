# api.py

import uuid
from constants import (
    ERROR_USER_NOT_FOUND,
    ERROR_MISSING_FIELDS,
    ERROR_MISSING_WORKOUT_FIELDS,
    ERROR_NOT_FOLLOWING,
)

class StravaLiteAPI:
    def __init__(self):
        # In-memory datastore for users.
        # Each user is a dictionary with keys: id, name, age, workouts, following.
        self.users = {}

    def register_user(self, name, age):
        """Registers a new user and returns the user object."""
        user_id = str(uuid.uuid4())
        user = {
            "id": user_id,
            "name": name,
            "age": age,
            "workouts": [],
            "following": []
        }
        self.users[user_id] = user
        return user

    def get_user(self, user_id):
        """Retrieves a user by id, or None if the user does not exist."""
        return self.users.get(user_id)

    def remove_user(self, user_id):
        """Removes a user from the datastore, returning the removed user or None if not found."""
        return self.users.pop(user_id, None)

    def list_users(self):
        """Returns a list of all users."""
        return list(self.users.values())

    def add_workout(self, user_id, date, time, distance):
        """Adds a workout for the specified user and returns the workout."""
        if user_id not in self.users:
            return None
        workout = {
            "date": date,
            "time": time,
            "distance": distance
        }
        self.users[user_id]["workouts"].append(workout)
        return workout

    def list_workouts(self, user_id):
        """Returns the list of workouts for the specified user, or None if the user does not exist."""
        if user_id not in self.users:
            return None
        return self.users[user_id]["workouts"]

    def follow_friend(self, user_id, follow_id):
        """Allows a user to follow another user, returning the updated following list."""
        if user_id not in self.users or follow_id not in self.users:
            return None
        if follow_id not in self.users[user_id]["following"]:
            self.users[user_id]["following"].append(follow_id)
        return self.users[user_id]["following"]

    def show_friend_workouts(self, user_id, follow_id):
        """
        Returns a friend's workouts if the current user is following the friend.
        If not following or the user does not exist, returns an error message.
        """
        if user_id not in self.users or follow_id not in self.users:
            return None, ERROR_USER_NOT_FOUND
        if follow_id not in self.users[user_id]["following"]:
            return None, ERROR_NOT_FOLLOWING
        return self.users[follow_id]["workouts"], None

# Global instance to be used in route handlers.
api = StravaLiteAPI()
