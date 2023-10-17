from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

import schemas
from database import get_db
from models import Book, User

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = "89fb49efe12df58cd7d49def9ef32c071fc6a23e2b2f941152101aae3184c8ea"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Counld not validate user")

        return {"username": username, "id": user_id}

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Counld not validate user")


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


@router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: schemas.CreateUserRequest):
    try:
        create_user_model = User(
            username=create_user_request.username,
            hashed_password=get_password_hash(create_user_request.password),
        )
        db.add(create_user_model)
        db.commit()
    except Exception:
        raise HTTPException(status_code=404, detail="Something went wrong")

    token = create_access_token(create_user_model.username, create_user_model.id, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}


def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"id": user_id, "sub": username}
    expires = datetime.utcnow() + expires_delta

    encode.update({"exp": expires})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    print("form_data---------", form_data)

    user = authenticate_user(form_data.username, form_data.password, db)
    print("user---------", user)

    if not user:
        print("if not user---------", user)

        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Counld not validate user")
    token = create_access_token(user.username, user.id, timedelta(days=1))

    print("token---------", token)

    return {"access_token": token, "token_type": "Bearer"}


@router.get("/me")
async def current_user(current_user: user_dependency, db: db_dependency):
    user = db.query(User).filter(User.id == current_user["id"]).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user": {"id": user.id, "username": user.username},
    }


@router.post("/logout")
async def logout(current_user: user_dependency):
    return {"message": "logged_out"}
