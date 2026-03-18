from fastapi import FastAPI
from app.api.v1 import user, auth

app = FastAPI(title="IMB Edu Platform API - Test IP Telephony")

app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(auth.router, prefix="/api/v1", tags=["Auth"])

@app.get("/")
async def root():
    return {"message": "API is running"}