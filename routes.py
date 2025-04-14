# routes.py

from flask import Flask, request, jsonify
from api import api
from constants import ERROR_USER_NOT_FOUND, ERROR_MISSING_FIELDS, ERROR_MISSING_WORKOUT_FIELDS, ERROR_NOT_FOLLOWING

def init_routes(app: Flask):
    @app.route('/user', methods=['POST'])
    def register_user():
        """
        Register a new user with a JSON payload containing 'name' and 'age'.
        """
        data = request.get_json()
        if not data or "name" not in data or "age" not in data:
            return jsonify({"error": ERROR_MISSING_FIELDS}), 400
        user = api.register_user(data["name"], data["age"])
        return jsonify(user), 200

    @app.route('/user/<user_id>', methods=['GET'])
    def get_user(user_id):
        """
        Retrieve a user's information by user ID.
        """
        user = api.get_user(user_id)
        if not user:
            return jsonify({"error": ERROR_USER_NOT_FOUND}), 404
        return jsonify(user), 200

    @app.route('/user/<user_id>', methods=['DELETE'])
    def remove_user(user_id):
        """
        Delete a user from the data store by user ID.
        """
        user = api.remove_user(user_id)
        if not user:
            return jsonify({"error": ERROR_USER_NOT_FOUND}), 404
        return '', 200

    @app.route('/users', methods=['GET'])
    def list_users():
        """
        List all registered users.
        """
        users = api.list_users()
        return jsonify({"users": users}), 200

    @app.route('/workouts/<user_id>', methods=['PUT'])
    def add_workout(user_id):
        """
        Add a workout for a specified user.
        Expects a JSON payload with 'date', 'time', and 'distance'.
        """
        data = request.get_json()
        required_fields = ["date", "time", "distance"]
        if not data or not all(field in data for field in required_fields):
            return jsonify({"error": ERROR_MISSING_WORKOUT_FIELDS}), 400
        workout = api.add_workout(user_id, data["date"], data["time"], data["distance"])
        if workout is None:
            return jsonify({"error": ERROR_USER_NOT_FOUND}), 404
        return jsonify(workout), 200

    @app.route('/workouts/<user_id>', methods=['GET'])
    def list_workouts(user_id):
        """
        Retrieve all workouts associated with a specified user.
        """
        workouts = api.list_workouts(user_id)
        if workouts is None:
            return jsonify({"error": ERROR_USER_NOT_FOUND}), 404
        return jsonify({"workouts": workouts}), 200

    @app.route('/follow-list/<user_id>', methods=['PUT'])
    def follow_friend(user_id):
        """
        Allow the current user to follow another user.
        Expects a JSON payload with 'follow_id'.
        """
        data = request.get_json()
        if not data or "follow_id" not in data:
            return jsonify({"error": "Missing 'follow_id' field"}), 400
        follow_id = data["follow_id"]
        following = api.follow_friend(user_id, follow_id)
        if following is None:
            return jsonify({"error": ERROR_USER_NOT_FOUND}), 404
        return jsonify({"following": following}), 200

    @app.route('/follow-list/<user_id>/<follow_id>', methods=['GET'])
    def show_friend_workouts(user_id, follow_id):
        """
        Retrieve the workouts of a friend if the current user is following them.
        Returns 403 if the user is not following the friend.
        """
        workouts, error = api.show_friend_workouts(user_id, follow_id)
        if error:
            if error == ERROR_NOT_FOLLOWING:
                return jsonify({"error": error}), 403
            else:
                return jsonify({"error": error}), 404
        return jsonify({"workouts": workouts}), 200
