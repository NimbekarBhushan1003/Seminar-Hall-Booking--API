import sys
import os
import pytest
import sqlite3

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
DB_PATH = "database/booking.db"

#2.Bug- Overlapping Booking Hall

@pytest.fixture(autouse=True)
def clear_booking_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM BOOKING")
    conn.commit()
    conn.close()