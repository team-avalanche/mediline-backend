from datetime import datetime, date
from enum import Enum

from typing import List, Optional

from beanie import Document, Indexed, Link, PydanticObjectId
from pydantic import BaseModel, EmailStr, Field

from api.utils.enum_types import AppointmentStatus


class AppointmentIn(BaseModel):
    # doctor_id: Indexed(PydanticObjectId)
    doctor_id: str
    date: date
    time_slot: int
    purpose: str


class Appointment(AppointmentIn, Document):
    # id: PydanticObjectId = Field(alias="_id")
    # patient_id: Indexed(PydanticObjectId)
    patient_id: str
    status: AppointmentStatus
