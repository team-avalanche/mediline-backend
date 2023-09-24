# define common profile fields

from pydantic import BaseModel

from api.utils.enum_types import Gender


class BaseProfile(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    gender: Gender | None = None
    contact: str | None = None
    address: str | None = None
