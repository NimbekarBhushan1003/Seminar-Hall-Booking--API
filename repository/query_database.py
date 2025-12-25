import sqlite3

class DB_Client:
    """
    Class for database client
    """
    def __init__(self):
        self.connection = sqlite3.connect('database/booking.db')

    def fetch_bookings(self, query_string):
        """
        Executes a sql query and returns list of all records from `BOOKING` table for this particular sql query
        param-
            query_string - string
        return -
            records - list
        """
        cursor = self.connection.execute(query_string)
        records = cursor.fetchall()
        return records
