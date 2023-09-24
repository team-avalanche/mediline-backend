from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from api.config import CONFIG
from api.models.user import UserInDB
from api.utils.enum_types import UserType
from api.utils.exceptions import (
    method_not_allowed_for_doctor,
    method_not_allowed_for_patient,
    user_not_active,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, CONFIG.secret_key, algorithms=[CONFIG.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception
    user = await UserInDB.by_email(email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: UserInDB = Depends(get_current_user),
) -> UserInDB:
    if current_user.disabled:
        raise user_not_active
    return current_user


gcu = get_current_user
gcau = get_current_active_user


ActiveUser = Annotated[UserInDB, Depends(get_current_active_user)]


async def get_doctor(current_active_user: ActiveUser) -> UserInDB:
    if current_active_user.user_type == UserType.doctor:
        return current_active_user
    raise method_not_allowed_for_patient


async def get_patient(current_active_user: ActiveUser) -> UserInDB:
    if current_active_user.user_type == UserType.patient:
        return current_active_user
    raise method_not_allowed_for_doctor


Doctor = Annotated[UserInDB, Depends(get_doctor)]
Patient = Annotated[UserInDB, Depends(get_patient)]
