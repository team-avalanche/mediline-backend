from enum import Enum


class UserType(str, Enum):
    doctor = "doctor"
    patient = "patient"


class AppointmentStatus(str, Enum):
    scheduled = "scheduled"
    cancelled = "cancelled"
    completed = "completed"


class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"
