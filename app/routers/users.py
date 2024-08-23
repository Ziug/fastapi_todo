from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

import schemas, models
from database import get_db
from utils import hash


router = APIRouter(prefix="/users", tags=["todo"])

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
async def create_user(new_user: schemas.UserCreate, db: Session = Depends(get_db)):

    new_user.password = await hash(new_user.password)
    created_user = models.User(**new_user.model_dump())
    
    try:
        db.add(created_user)
        db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This username is taken")
    db.refresh(created_user)

    return created_user