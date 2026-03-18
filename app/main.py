from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1 import auth, user, admin
from app.core.redis import init_redis, close_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_redis()
    yield
    await close_redis()


app = FastAPI(
    lifespan=lifespan,
    title="IMB Edu Platform API - Test IP Telephony"
)
app.include_router(auth.router, prefix="/api/v1", tags=["Auth"])
app.include_router(user.router, prefix="/api/v1", tags=["User"])
app.include_router(admin.router, prefix="/api/v1", tags=["Admin"])

@app.get("/")
async def root():
    return {"message": "API is running"}