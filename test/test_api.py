import requests
from pprint import pprint

BASE = "http://localhost:8085"

r = requests.get(f"{BASE}/bookings")
pprint(r.json())

