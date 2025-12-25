import enum

class Halls(enum.Enum):
    """
    Class for storing hall capacity
    Access the hall capacity using -
        `Halls.A.value` will be 50
        `Halls.B.value` will be 100
    """
    A = 50
    B = 100
    C = 200
    D = 350
    E = 500
    F = 1000
