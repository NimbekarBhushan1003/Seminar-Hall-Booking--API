class Booking:
    """
    Class to store the booking information
    """
    def __init__(self, id, hall_name, capacity, start_time, end_time):
        """
        param -
            id = string
            hall_name = string
            capacity = integer
            start_time = datetime
            end_time = datetime
        """
        self.id = id
        self.hall_name = hall_name
        self.capacity = capacity
        self.start_time = start_time
        self.end_time = end_time
