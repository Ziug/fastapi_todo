from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

import schemas, models
from database import get_db
from utils import hash


router = APIRouter(prefix="/users", tags=["todo"])

# ============================================ create ============================================
@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(new_user: schemas.UserCreate, db: Session = Depends(get_db)):
    usr_exists = db.query(models.User).filter(models.User.username == new_user.username).first()
    
    if usr_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This username is taken")

    new_user.password = await hash(new_user.password)
        
    created_user = models.User(**new_user.model_dump())
    
    try:
        db.add(created_user)
        db.commit()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user")
    db.refresh(created_user)

    return created_user

# Todo - login and jwt token functionality