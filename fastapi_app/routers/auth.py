from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends()
):
    #Preferred: OAuth2 / Form login
    username = form_data.username
    password = form_data.password

    #Fallback: query params (old Flask-style tests)
    if not username or not password:
        username = request.query_params.get("username")
        password = request.query_params.get("password")

    if not username or not password:
        raise HTTPException(status_code=422, detail="Username and password required")

    # TEMP auth logic (same as Flask)
    token = create_access_token({"sub": username})
    return {
        "access_token": token,
        "token_type": "bearer"
    }
