from fastapi import HTTPException, status
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def hash(password: str):
    return pwd_context.hash(password)


async def verify(user_provided, hashed_pass):
    return pwd_context.verify(user_provided, hashed_pass)
