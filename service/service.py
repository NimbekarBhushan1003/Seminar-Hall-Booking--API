import sqlite3
from datetime import datetime
import uuid

DB_PATH = "database/booking.db"

HALLS = [
    {"name": "A", "capacity": 50},
    {"name": "B", "capacity": 100},
    {"name": "C", "capacity": 200},
    {"name": "D", "capacity": 350},
    {"name": "E", "capacity": 500},
    {"name": "F", "capacity": 1000},
]

# ---------- FETCH BOOKINGS ----------
def fetch_all_bookings():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM BOOKING")
    rows = cur.fetchall()
    conn.close()

    return [
        {
            "id": r[0],
            "hallName": r[1],
            "capacity": r[2],
            "startTime": r[3],
            "endTime": r[4],
        }
        for r in rows
    ]


# ---------- AVAILABLE HALLS ----------
def get_available_halls(capacity, start, end):
    start_dt = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT HALL_NAME, START_TIME, END_TIME FROM BOOKING")
    bookings = cur.fetchall()
    conn.close()

    available = []

    for hall in sorted(HALLS, key=lambda h: h["capacity"]):
        if hall["capacity"] >= capacity:
            conflict = False
            for h, s, e in bookings:
                if h == hall["name"]:
                    if max(start_dt, datetime.fromisoformat(s)) < min(end_dt, datetime.fromisoformat(e)):
                        conflict = True
                        break
            if not conflict:
                available.append(hall["name"])

    return available


# ---------- BOOK BEST FIT ----------
def book_best_fit_hall(capacity, start, end):
    available = get_available_halls(capacity, start, end)
    if not available:
        return None

    hall_name = available[0]
    hall_capacity = next(h["capacity"] for h in HALLS if h["name"] == hall_name)
    booking_id = str(uuid.uuid4())[:8]

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO BOOKING VALUES (?, ?, ?, ?, ?)",
        (booking_id, hall_name, hall_capacity, start, end)
    )
    conn.commit()
    conn.close()

    return hall_name
