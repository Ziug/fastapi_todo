from datetime import datetime, timedelta, timezone

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

import models, jwt
from database import get_db
from schemas import TokenData
from config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = f"{settings.secret_key}"
ALGORITHM = f"{settings.algorithm}"
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.access_token_expire_minutes)


async def create_access_token(data: dict):
    to_encode = data.copy()

    # expire in Moscow timezone, cause server uses Moscow time :)
    expire = datetime.now(timezone(timedelta(hours=3))) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
)

    to_encode.update({"exp": expire})

    encoded = jwt.encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

    return encoded


async def verify_access_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id")

        if not id:
            raise credentials_exception

        token_data = TokenData(id=id)

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not logged in")

    except jwt.InvalidTokenError:
        raise credentials_exception    

    return token_data


async def get_curr_usr(token_data: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    token = await verify_access_token(token_data)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    return user