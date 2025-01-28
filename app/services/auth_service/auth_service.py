import jwt  # Don't forget to import jwt
from datetime import datetime, timedelta
from app.core.config import settings
from typing import Optional
from jwt.exceptions import PyJWTError


class AuthService:
    def __init__(self):
        pass

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        if expires_delta is None:
            expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)  
        expiration = datetime.utcnow() + expires_delta
        to_encode = data.copy()
        to_encode.update({"exp": expiration}) 
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)  
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])  
            return payload
        except PyJWTError:
            return None
