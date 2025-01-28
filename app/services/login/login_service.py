from http.client import HTTPException
from app.services.auth_service.auth_service import AuthService
from app.core.config import settings


class loginService:
    def login_service(self, username: str, password: str) -> str:
        if username == settings.USER and password == settings.PASSWORD:
            user_data = {"sub": username}
            auth_service = AuthService()  
            access_token = auth_service.create_access_token(data=user_data)  
            return access_token
        else:
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")