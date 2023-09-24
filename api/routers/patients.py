from fastapi import APIRouter

from api.models.patients import PatientProfile, PatientProfileIn
from api.utils.current_user import Patient
from api.utils.exceptions import patient_profile_not_found_exc

router = APIRouter(prefix="/patient", tags=["Patients"])


@router.get("/profile")
async def get_patient_profile(user: Patient) -> PatientProfile:
    return await PatientProfile.find_one(PatientProfile.id == user.id)


@router.patch("/profile")
async def update_patient_profile(profile_update: PatientProfileIn, user: Patient):
    patient = await PatientProfile.find_one(PatientProfile.id == user.id)
    if not patient:
        raise patient_profile_not_found_exc
    patient = await patient.model_copy(
        update=profile_update.model_dump(exclude_unset=True)
    )
    await patient.save()

    return patient.id
