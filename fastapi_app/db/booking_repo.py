import sqlite3
import uuid
from fastapi import HTTPException
from fastapi_app.schemas.booking import BookingCreate

DB_PATH = "database/booking.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_booking(booking: BookingCreate):
    booking_id = str(uuid.uuid4())

    conn = get_connection()
    cursor = conn.cursor()

    # CHECK FOR OVERLAPPING BOOKINGS(2-bug resolution)
    cursor.execute("""
        SELECT START_TIME, END_TIME
        FROM BOOKING
        WHERE HALL_NAME = ?
          AND NOT (
              END_TIME <= ?
              OR START_TIME >= ?
          )
    """, (
        booking.hall_name,
        booking.start_time.isoformat(),
        booking.end_time.isoformat()
    ))

    overlap = cursor.fetchone()
    if overlap:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="Booking overlaps with existing booking"
        )

    cursor.execute("""
        INSERT INTO BOOKING (ID, HALL_NAME, CAPACITY, START_TIME, END_TIME)
        VALUES (?, ?, ?, ?, ?)
    """, (
        booking_id,
        booking.hall_name,
        booking.capacity,
        booking.start_time.isoformat(),
        booking.end_time.isoformat()
    ))

    conn.commit()
    conn.close()

    return {
        "id": booking_id,
        **booking.model_dump()
    }

def get_all_bookings():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM BOOKING")
    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "id": r[0],
            "hall_name": r[1],
            "capacity": r[2],
            "start_time": r[3],
            "end_time": r[4]
        }
        for r in rows
    ]

def delete_booking(booking_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM BOOKING WHERE ID = ?", (booking_id,))
    deleted = cursor.rowcount

    conn.commit()
    conn.close()

    return deleted > 0
