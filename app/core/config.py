from decouple import config

DATABASE_URL = config("DATABASE_URL")

REDIS_URL = config("REDIS_URL", default="redis://localhost:6379")

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=60, cast=int)
REFRESH_TOKEN_EXPIRE_DAYS = config("REFRESH_TOKEN_EXPIRE_DAYS", default=7, cast=int)

OTP_LIFE_TIME = 120
