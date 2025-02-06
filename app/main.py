from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from app.models import Base
from app.database import engine
from app.routers import contacts, auth, reset_password, user_roles, jwt_refresh_tokens
from app.config import settings
from app.limiter import add_rate_limit_middleware
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address


app = FastAPI()
limiter = Limiter(key_func=get_remote_address)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_rate_limit_middleware(app)

@app.get("/")
@limiter.limit("5/minute")
def read_root():
    return {"message": "API work!"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ The database has been initialized successfully!")

# Маршруты
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(reset_password.router, prefix="/auth/password-reset", tags=["Password Reset"])  # Изменили префикс
app.include_router(user_roles.router, tags=["User Roles"])
app.include_router(jwt_refresh_tokens.router, tags=["Auth"])
app.include_router(contacts.router, prefix="/contacts", tags=["Contacts"])

# Обработчик ошибок Rate Limit
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"error": "Rate limit exceeded. Please try again later."}
    )
