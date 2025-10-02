from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated

from app.api.models.user import User
from app.db.database import get_db
from app.utils.jwt_helpers import verify_jwt_token
from app.core import response_messages



oauth_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    db: Annotated[Session, Depends(get_db)],
    access_token: Annotated[str, Depends(oauth_scheme)],
) -> User:
    """Dependency to get current logged in user
    Useful for protecting routes and restricting their access to only
    authenticated users

    Args:
        db (Annotated[Session, Depends): Database Session
        access_token (Annotated[str, Depends): JWT access token

    Returns:
        User: Logged in User object
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=response_messages.INVALID_CREDENTIALS,
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_id = verify_jwt_token(
        token=access_token, credentials_exception=credentials_exception
    )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise credentials_exception

    return user

def get_current_admin_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Dependency to get current logged in admin user
    Useful for protecting routes and restricting their access to only
    authenticated admin users

    Args:
        current_user (Annotated[User, Depends): Current logged in user

    Returns:
        User: Logged in admin User object
    """

    if not current_user.role == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=response_messages.ADMIN_PRIVILEGES_REQUIRED,
        )

    return current_user