from datetime import datetime, date


# from api.models.classroom import Classroom
from typing import List, Optional, Dict

from beanie import Document, Indexed, Link
from pydantic import BaseModel, EmailStr, Field
from beanie import PydanticObjectId
from api.utils.enum_types import Gender


class DoctorProfileIn(BaseModel):
    gender: Gender | None
    contact: str | None
    hospital: str | None
    specialization: str | None
    clinic_address: str | None


class DoctorAvailability(Document):
    # id: PydanticObjectId = Field(alias="_id")
    doctor_availability: Dict[int, Dict[int, int]] | None


class DoctorProfile(DoctorProfileIn, Document):
    # id: PydanticObjectId = Field(alias="_id")

    pass
