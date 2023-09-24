from typing import Dict

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field

from api.models.profile import BaseProfile


class DoctorProfileIn(BaseProfile):
    hospital: str | None = None
    specialization: str | None = None
    clinic_address: str | None = None


# class DoctorAvailabilityInSchema(BaseModel):
#     doctor_availability: Dict[
#         conint(ge=0, le=6), Dict[conint(ge=0, le=23), conint(ge=0, le=100)]
#     ] | None = None


# some jugaad going on
class DoctorAvailabilityInSchema(BaseModel):
    doctor_availability: Dict[str, Dict[str, int]] | None = None


class DoctorAvailability(Document):
    id: PydanticObjectId = Field(alias="_id")
    doctor_availability: Dict[str, Dict[str, int]] | None = {}


class DoctorProfile(DoctorProfileIn, Document):
    id: PydanticObjectId = Field(alias="_id")
