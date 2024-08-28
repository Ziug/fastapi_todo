from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import oauth2, utils, models
from database import get_db

router = APIRouter(prefix="/login", tags=["auth"])


@router.post("")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_to_login = db.query(models.User).filter(models.User.username == form_data.username).first()
    
    if not user_to_login:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    
    if not await utils.verify(user_provided=form_data.password, hashed_pass=user_to_login.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    
    access_token = await oauth2.create_access_token(data={"user_id": user_to_login.id})
    return {"access_token": access_token, "token_type": "bearer"}