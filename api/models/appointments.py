from datetime import date

from beanie import Document, PydanticObjectId
from pydantic import BaseModel

from api.utils.enum_types import AppointmentStatus


class AppointmentIn(BaseModel):
    doctor_id: PydanticObjectId
    date: date
    time_slot: int
    purpose: str

    class Settings:
        bson_encoders = {date: str}


class Appointment(AppointmentIn, Document):
    patient_id: PydanticObjectId
    status: AppointmentStatus
