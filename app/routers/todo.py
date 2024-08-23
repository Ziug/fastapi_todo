from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import sys
sys.path.append("..")

from models import TodoTask
from database import get_db


router = APIRouter(prefix="/todo", tags=["todo"])


# ============================================ get ============================================
@router.get("")
async def get_all(db: Session = Depends(get_db)):
    return db.query(TodoTask).all()

# ============================================ create ============================================

