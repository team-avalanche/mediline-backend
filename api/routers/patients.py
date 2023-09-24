from beanie import PydanticObjectId
from fastapi import APIRouter

from api.models.appointments import Appointment
from api.models.patients import PatientProfile, PatientProfileIn
from api.utils.current_user import Doctor, Patient
from api.utils.enum_types import AppointmentStatus
from api.utils.exceptions import patient_profile_not_found_exc

router = APIRouter(prefix="/patient", tags=["Patients"])


@router.get("/my-profile")
async def get_patient_self_profile(user: Patient) -> PatientProfile:
    return await PatientProfile.find_one(PatientProfile.id == user.id)


@router.patch("/my-profile")
async def update_patient_self_profile(profile_update: PatientProfileIn, user: Patient):
    patient = await PatientProfile.find_one(PatientProfile.id == user.id)
    if not patient:
        raise patient_profile_not_found_exc
    patient = await patient.model_copy(
        update=profile_update.model_dump(exclude_unset=True)
    )
    await patient.save()

    return patient.id


async def get_patient_profile(
    patient_id: PydanticObjectId, user: Doctor
) -> PatientProfile:
    # privacy
    # a doctor who has atleast appointment with patient will be able to view his profile
    aptmnts = Appointment.find_many(
        Appointment.doctor_id == user.id,
        Appointment.status != AppointmentStatus.cancelled,
    )
    if len(aptmnts) > 0:
        patient_profile = await PatientProfile.find_one(PatientProfile.id == patient_id)
        if not patient_profile:
            raise patient_profile_not_found_exc
        return patient_profile
