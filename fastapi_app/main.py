from fastapi import FastAPI
from fastapi_app.routers.booking import router as booking_router
from fastapi_app.routers.auth import router as auth_router

app = FastAPI(title="Booking API--FastAPI Version")

@app.get("/", tags=["Health Check"])
def health_check():
    return {"message": "Checking"}

#  REGISTER ROUTER
app.include_router(booking_router)
app.include_router(auth_router)
