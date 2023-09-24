from typing import Dict

from beanie import Document, PydanticObjectId
from pydantic import Field

from api.models.profile import BaseProfile


class DoctorProfileIn(BaseProfile):
    hospital: str | None = None
    specialization: str | None = None
    clinic_address: str | None = None


class DoctorAvailability(Document):
    id: PydanticObjectId = Field(alias="_id")
    doctor_availability: Dict[int, Dict[int, int]] | None = None


class DoctorProfile(DoctorProfileIn, Document):
    id: PydanticObjectId = Field(alias="_id")
