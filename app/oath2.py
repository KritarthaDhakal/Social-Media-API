from jose import jwt, JWTError
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
EXPIRE_TIME_MIN = settings.access_token_expire_minutes

oath2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRE_TIME_MIN)
    to_encode.update({'exp': expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_acess_token(token: str, credentials_exception):
    
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get('user_id')
        if not payload:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(token: str = Depends(oath2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Unauthorized Access.", headers={'WWW.Authenticate': 'Bearer'})
    token_data = verify_acess_token(token, credentials_exception)
    user = db.query(models.User).filter(token_data.id == models.User.id).first()
    return user

