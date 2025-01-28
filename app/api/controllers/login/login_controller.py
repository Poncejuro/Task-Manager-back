from fastapi import APIRouter, HTTPException, Depends
from app.services.login.login_service import loginService
from app.api.schemas.TokenSchemas import TokenRequest, TokenResponse

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
async def login_for_access_token(request: TokenRequest, login_service: loginService = Depends(loginService)):
    access_token = login_service.login_service(request.username, request.password)
    return {"access_token": access_token, "token_type": "bearer"}