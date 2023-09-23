from datetime import datetime, date


from typing import List, Optional

from beanie import Document, Indexed, Link, PydanticObjectId
from api.utils.enum_types import Gender

from pydantic import BaseModel, Field


class PatientProfileIn(BaseModel):
    gender: Gender
    dob: date
    contact: str
    address: str


class PatientProfile(PatientProfileIn, Document):
    # id: PydanticObjectId = Field(alias="_id")
    pass
