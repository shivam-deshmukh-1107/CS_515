# Strava Lite

[GitHub Repository](https://github.com/shivam-deshmukh-1107/Shivam_Deshmukh_CS_515)

**Author:** Your Name – [sdeshmuk2@stevens.edu](mailto:sdeshmuk2@stevens.edu)

## Project Description

Strava Lite is a lightweight Flask server application that allows users to register, log their running workouts, and interact socially by following friends. Users can:
- Register and manage their accounts.
- Add and list workout entries.
- Follow other users and view their workout activities (extra credit social features).

## Features

- **User Management:**
  - **Register User:** `POST /user`
  - **Get User:** `GET /user/<user_id>`
  - **Remove User:** `DELETE /user/<user_id>`
  - **List Users:** `GET /users`
  
- **Workout Management:**
  - **Add Workout:** `PUT /workouts/<user_id>`
  - **List Workouts:** `GET /workouts/<user_id>`
  
- **Social Features (Extra Credit):**
  - **Follow Friend:** `PUT /follow-list/<user_id>`
  - **Show Friend Workouts:** `GET /follow-list/<user_id>/<follow_id>`

## Setup Instructions

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/your-username/your-repository.git
    ```
2. **Create and Activate a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # For Windows: venv\Scripts\activate
    ```
3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Run the Application:**
    ```bash
    python app.py
    ```
    The server will run at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Running Tests

To run the tests, execute:
```bash
python test.py
