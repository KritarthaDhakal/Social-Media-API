from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils 
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['User']
)


# func for creating a user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(new_user: schemas.UserModel, db: Session = Depends(get_db)):
    
    new_user.password = utils.hashing(new_user.password)
    
    user = models.User(**new_user.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# func for getting a user's info
@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} was not found.")
    return user