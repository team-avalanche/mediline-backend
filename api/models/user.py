from datetime import datetime

# from api.models.classroom import Classroom
from typing import Optional

from beanie import Document
from pydantic import BaseModel, EmailStr

from api.utils.enum_types import UserType


class UserAuth(BaseModel):
    # what comes in user login form
    email: EmailStr
    password: str
    user_type: UserType


class UserUpdate(BaseModel):
    # what comes in user update request
    email: EmailStr | None = None


class UserOut(UserUpdate):
    # what is given in response
    # email: Indexed(str, unique=True)
    email: EmailStr
    # why Indexed(EmailStr) didnt work here
    # TODO: find original source from where I earlier wrote this
    # implications of removing EmailStr
    # keyerror

    disabled: bool = False


class UserInDB(UserOut, Document):
    # what is stored in db
    user_type: UserType
    hashed_password: str
    email_confirmed_at: Optional[datetime] = None

    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def __str__(self) -> str:
        return str(self.email)

    def __hash__(self) -> int:
        return hash(self.email)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, UserInDB):
            return self.email == other.email
        return False

    @property
    def created(self) -> datetime:
        return self.id.generation_time

    @classmethod
    async def by_email(cls, email: str) -> "UserInDB":
        return await cls.find_one(cls.email == email)
