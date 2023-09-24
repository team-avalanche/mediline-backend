from datetime import date

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field

from api.utils.enum_types import Gender


class PatientProfileIn(BaseModel):
    gender: Gender | None = None
    dob: date | None = None
    contact: str | None = None
    address: str | None = None


class PatientProfile(PatientProfileIn, Document):
    id: PydanticObjectId = Field(alias="_id")
