from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api.user.repository import create_user, get_user_by_username
from api.user.schema import User, UserCreate
from core.database.session import get_db
from core.oauth.oauth import authenticate_user, create_access_token
from core.settings.logging import setup_logging


oauth = APIRouter()
logger = setup_logging()


@oauth.post("/register", response_model=User)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Registration attempt for user: {user.username}")
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        logger.warning(f"Registration attempt with existing user: {user.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already registered"
        )
    return create_user(db=db, user=user)

@oauth.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    logger.info(f"Login attempt for user: {form_data.username}")
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.warning(f"Failed login attempt for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    logger.info(f"Successful login for user: {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer"}
