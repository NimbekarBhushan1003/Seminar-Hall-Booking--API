from pydantic import BaseModel, Field, model_validator
from datetime import datetime, timezone


class BookingCreate(BaseModel):
    hall_name: str
    capacity: int = Field(gt=0, le=500)
    start_time: datetime
    end_time: datetime

    @model_validator(mode="after")
    def validate_time(self):
        # End time must be after start time
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")

        # Normalize timezone
        start = (
            self.start_time.replace(tzinfo=timezone.utc)
            if self.start_time.tzinfo is None
            else self.start_time
        )

        now = datetime.now(timezone.utc)

        if start < now:
            raise ValueError("Booking cannot be in the past")

        return self


class BookingResponse(BookingCreate):
    id: str
