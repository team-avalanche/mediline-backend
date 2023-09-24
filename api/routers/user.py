from fastapi import APIRouter, HTTPException, status

from api.models.user import UserOut, UserUpdate
from api.utils.current_user import ActiveUser

router = APIRouter(prefix="/user", tags=["User"])


@router.get("")
async def get_user(user: ActiveUser) -> UserOut:
    return user


@router.patch("")
async def update_user(update: UserUpdate, user: ActiveUser) -> UserOut:
    user = user.model_copy(update=update.model_dump(exclude_unset=True))
    try:
        await user.save()
    except Exception as exc:
        if type(exc).__name__ == "DuplicateKeyError":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="DuplicateKeyError: Another user exists with this email",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Please provide valid values or try again later",
            )

    return user


# update email should have a different route, as we need to except duplicate email case,
# and also send verification link
