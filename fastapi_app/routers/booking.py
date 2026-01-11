from fastapi import APIRouter, Depends
from uuid import uuid4

from fastapi_app.schemas.booking import BookingCreate, BookingResponse
from fastapi_app.dependencies.auth import get_current_user

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)

# In-memory DB
bookings_db = []


@router.post("/", response_model=BookingResponse, status_code=201)
def create_booking(
    booking: BookingCreate,
    user=Depends(get_current_user)
):
    booking_data = {
        "id": str(uuid4()),
        **booking.model_dump()
    }
    bookings_db.append(booking_data)
    return booking_data


@router.get("/", status_code=200)
def list_bookings(user=Depends(get_current_user)):
    return bookings_db

