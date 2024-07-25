import pytest
import requests
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

sys.path.append(parent_dir)

from app.models.models import User

BASE_URL = "http://localhost:8000/api/v1/users"

NEW_USER_DATA = {
    "first_name": "Jane",
    "last_name": "Smith",
    "address": "456 Oak St",
    "phone_number": "0987654321",
    "email": "jane@example.com",
    "hashed_password": "password",
    "reward_requested": True
}

FIRST_USER_DATA = {
    "user_id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "address": "123 Main St, City",
    "phone_number": "1234567890",
    "email": "john@example.com",
    "hashed_password": "password",
    "reward_requested": False
}

@pytest.fixture
def test_get_all_users():
    response = requests.get(BASE_URL + "/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def create_and_delete_user():
    response = requests.post(BASE_URL + "/", json=NEW_USER_DATA)
    assert response.status_code == 200
    created_user_id = response.json().get("user_id")
    yield created_user_id
    response = requests.delete(BASE_URL + f"/{created_user_id}")
    assert response.status_code == 200

def test_get_user_by_id():
    response = requests.get(BASE_URL + f"/1")
    assert response.status_code == 200
    user_data = response.json()
    retrieved_user = User(**user_data)
    assert retrieved_user == User(**FIRST_USER_DATA)

def test_update_user():
    updated_user_data = FIRST_USER_DATA.copy()
    updated_user_data["first_name"] = "Updated John"
    response = requests.put(BASE_URL + f"/1", json=updated_user_data)
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["first_name"] == "Updated John"
    assert updated_user["last_name"] == FIRST_USER_DATA["last_name"]

    # Revert the changes to keep the database state consistent
    response = requests.put(BASE_URL + f"/1", json=FIRST_USER_DATA)
    assert response.status_code == 200
    reverted_user = response.json()
    assert reverted_user == FIRST_USER_DATA
