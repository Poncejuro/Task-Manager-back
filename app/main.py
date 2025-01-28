from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.dataBases.postgresDb import create_schema, create_db_tables
from app.api.controllers.task.task_controller import router as task_router 
from app.api.controllers.login.login_controller import router as login_router 
from app.core.middleware.auth import JWTAuthenticationMiddleware
from app.core.middleware.errorHandling import ErrorHandlingMiddleware
from starlette.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_schema()  
    await create_db_tables()  
    yield
    print("Application is shutting down...")

app = FastAPI(lifespan=lifespan)


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  
#     allow_credentials=True,
#     allow_methods=["*"], 
#     allow_headers=["*"], 
# )

app.add_middleware(JWTAuthenticationMiddleware)
app.add_middleware(ErrorHandlingMiddleware)

app.include_router(task_router, prefix="/v1")
app.include_router(login_router, prefix="/v1")