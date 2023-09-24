from datetime import date

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field

from api.utils.enum_types import AppointmentStatus


class AppointmentIn(BaseModel):
    doctor_id: PydanticObjectId
    date: date
    time_slot: int
    purpose: str


class Appointment(AppointmentIn, Document):
    id: PydanticObjectId = Field(alias="_id")
    patient_id: PydanticObjectId
    status: AppointmentStatus
