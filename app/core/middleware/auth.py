from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.services.auth_service.auth_service import AuthService

class JWTAuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            return await call_next(request)
        
        if request.url.path == "/v1/login":
            return await call_next(request)

        token = request.headers.get("Authorization")
        
        if not token:
            raise HTTPException(status_code=401, detail="Falta el token de autorización")
        
        token = token.replace("Bearer ", "")
        
        try:
            auth = AuthService()
            payload = auth.verify_token(token)
            if payload is None:
                raise HTTPException(status_code=401, detail="Token inválido o manipulado")
            
            request.state.user = payload
        except HTTPException:
            raise HTTPException(status_code=401, detail="Token inválido o expirado")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
        response = await call_next(request)
        return response
