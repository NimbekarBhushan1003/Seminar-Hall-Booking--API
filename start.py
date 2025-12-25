import sqlite3
from datetime import datetime
from controller.controller import app

PORT = 8085

def initialize_database():
    connection = sqlite3.connect('database/booking.db')
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS BOOKING (
            ID TEXT PRIMARY KEY,
            HALL_NAME TEXT NOT NULL,
            CAPACITY INTEGER NOT NULL,
            START_TIME TEXT NOT NULL,
            END_TIME TEXT NOT NULL
        )
    """)

    # Seed data only if table empty
    cursor.execute("SELECT COUNT(*) FROM BOOKING")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO BOOKING VALUES (?, ?, ?, ?, ?)",
            [
                ("2546543", "A", 50, "2021-06-27 15:00:00", "2021-06-27 16:00:00"),
                ("2546541", "A", 50, "2021-06-27 16:00:00", "2021-06-27 17:00:00"),
                ("2546542", "B", 100, "2021-06-27 16:00:00", "2021-06-27 17:00:00"),
                ("2546544", "C", 200, "2021-06-27 16:30:00", "2021-06-27 17:30:00")
            ]
        )

    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=PORT, debug=True)

