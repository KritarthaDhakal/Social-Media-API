from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, utils, models, oath2
from ..database import get_db

router = APIRouter(
    tags=["Authenticate"]
    )

@router.post("/login", response_model=schemas.Token)
def user_login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(credentials.username == models.User.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials.")
    if not utils.verifying(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials.")
    
    access_token = oath2.create_access_token({'user_id': user.id})
    return {"access_token": access_token, "token_type": "bearer"}