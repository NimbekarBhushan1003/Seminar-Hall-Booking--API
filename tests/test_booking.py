from fastapi.testclient import TestClient
from fastapi_app.main import app
from datetime import datetime, timedelta, timezone

client = TestClient(app)


def get_token():
    response = client.post(
        "/auth/login",
        data={"username": "test", "password": "test"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]

#1.Bug- Unauthorized access test

def test_wrong_authorization_header_returns_401():
    token = get_token()

    response = client.get(
        "/bookings/",
        headers={"Authorzation": f"Bearer {token}"}  # intentional typo
    )

    assert response.status_code == 401

#3.Bug- Capacity Edge Case
def test_booking_invalid_capacity():
    token = get_token()

    res = client.post(
        "/bookings/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "hall_name": "Bad Capacity Hall",
            "capacity": 0,
            "start_time": "2026-01-10T10:00:00",
            "end_time": "2026-01-10T11:00:00"
        }
    )

    assert res.status_code == 422

#4.Bug - a) End time before start time
def test_booking_end_before_start():
    token = get_token()

    res = client.post(
        "/bookings/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "hall_name": "Invalid Time Hall",
            "capacity": 20,
            "start_time": "2026-01-10T11:00:00",
            "end_time": "2026-01-10T10:00:00"
        }
    )

    assert res.status_code == 422

#4.Bug - b) Same start time & end time
def test_booking_same_start_end_time():
    token = get_token()

    res = client.post(
        "/bookings/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "hall_name": "Zero Duration Hall",
            "capacity": 20,
            "start_time": "2026-01-10T10:00:00",
            "end_time": "2026-01-10T10:00:00"
        }
    )

    assert res.status_code == 422

#4.Bug - c) Booking in the past
def test_booking_in_past():
    token = get_token()
    past = datetime.now(timezone.utc) - timedelta(days=1)

    res = client.post(
        "/bookings/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "hall_name": "Past Hall",
            "capacity": 10,
            "start_time": past.isoformat(),
            "end_time": (past + timedelta(hours=1)).isoformat()
        }
    )

    assert res.status_code == 422
