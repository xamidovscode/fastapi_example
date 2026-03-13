from fastapi import FastAPI
from app.api.v1 import user

app = FastAPI(title="Edu Platform API - Test Skeleton")

# Routers
app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])

@app.get("/")
async def root():
    return {"message": "API is running"}