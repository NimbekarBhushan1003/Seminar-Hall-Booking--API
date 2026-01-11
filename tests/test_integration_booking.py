from fastapi.testclient import TestClient
from fastapi_app.main import app

client = TestClient(app)

def test_integration_create_and_list_booking():
    login_res = client.post(
        "/auth/login",
        data={"username": "admin", "password": "admin"}  # ✅ FIX
    )
    assert login_res.status_code == 200

    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    create_res = client.post(
        "/bookings/",
        headers=headers,
        json={
            "hall_name": "Integration Hall",
            "capacity": 100,
            "start_time": "2026-01-15T10:00:00",
            "end_time": "2026-01-15T11:00:00"
        }
    )
    assert create_res.status_code == 201

    list_res = client.get("/bookings/", headers=headers)
    assert list_res.status_code == 200
