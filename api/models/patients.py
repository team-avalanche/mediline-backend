from datetime import date

from beanie import Document, PydanticObjectId
from pydantic import Field

from api.models.profile import BaseProfile


class PatientProfileIn(BaseProfile):
    dob: date | None = None
    blood_group: str | None = None

    class Settings:
        bson_encoders = {date: str}


class PatientProfile(PatientProfileIn, Document):
    id: PydanticObjectId = Field(alias="_id")
