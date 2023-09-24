from fastapi import APIRouter, HTTPException

from api.models.doctors import DoctorAvailability, DoctorProfile
from api.models.patients import PatientProfile
from api.models.user import UserAuth, UserInDB, UserOut
from api.utils.enum_types import UserType

# from api.utils.mail import send_password_reset_email
from api.utils.password import get_password_hash

router = APIRouter(prefix="/register", tags=["User Registration"])


@router.post("", response_model=UserOut)
async def user_registration(user_auth: UserAuth):
    user = await UserInDB.by_email(user_auth.email)
    if user is not None:
        raise HTTPException(409, "This email is already registered with another user")
    hashed = get_password_hash(user_auth.password)
    user = UserInDB(
        email=user_auth.email, hashed_password=hashed, user_type=user_auth.user_type
    )
    await user.create()
    if user.user_type == UserType.doctor:
        profile = DoctorProfile(id=user.id)
        avlb = DoctorAvailability(id=user.id)
        await avlb.create()
    else:
        profile = PatientProfile(id=user.id)
    await profile.create()

    return user


# to be implemented
# forgot password
# reset password
# verify email
