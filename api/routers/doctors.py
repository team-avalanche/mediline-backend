from beanie import PydanticObjectId
from fastapi import APIRouter

from api.models.doctors import DoctorAvailability, DoctorProfile, DoctorProfileIn
from api.utils.current_user import ActiveUser, Doctor
from api.utils.exceptions import (
    doc_avlb_details_not_found_exc,
    doc_profile_not_found_exc,
)

router = APIRouter(prefix="/doctor", tags=["Doctors"])


@router.get("/get-all-doctors")
async def get_all_doctors(user: ActiveUser):
    return await DoctorProfile.find_all().to_list()


@router.get("/get-doctor-profile")
async def get_doctor_profile(doctor_id: PydanticObjectId, user: ActiveUser):
    doctor_profile = DoctorProfile.find_one(DoctorProfile.id == doctor_id)
    if not doctor_profile:
        raise doc_profile_not_found_exc
    return doctor_profile


@router.get("/get-doctor-availability")
async def get_doctor_availability(doctor_id: PydanticObjectId, user: ActiveUser):
    doc_avlb = DoctorAvailability.find_one(DoctorProfile.id == doctor_id)
    if not doc_avlb:
        raise doc_avlb_details_not_found_exc
    return doc_avlb


@router.get("/my-profile")
async def get_doctor_self_profile(user: Doctor) -> DoctorProfile:
    doctor = DoctorProfile.find_one(DoctorProfile.id == user.id)
    if not doctor:
        raise doc_profile_not_found_exc
    return doctor


@router.patch("/my-profile")
async def update_doctor_self_profile(
    profile_details: DoctorProfileIn, user: Doctor
) -> PydanticObjectId:
    doctor = DoctorProfile.find_one(DoctorProfile.id == user.id)
    if not doctor:
        raise doc_profile_not_found_exc
    doctor = doctor.copy(update=profile_details.model_dump(exclude_unset=True))
    await doctor.save()
    return doctor.id


@router.get("/my-availability")
async def get_doctor_self_availability(user: Doctor) -> DoctorAvailability:
    doc_avlb = DoctorAvailability.find_one(DoctorAvailability.id == user.id)
    if not doc_avlb:
        raise doc_avlb_details_not_found_exc
    return doc_avlb


@router.patch("/my-availability")
async def update_doctor_self_availability(
    doc_avlb_update: DoctorAvailability, user: Doctor
) -> PydanticObjectId:
    doc_avlb = DoctorAvailability.find_one(DoctorProfile.id == user.id)
    if not doc_avlb:
        raise doc_avlb_details_not_found_exc

    doc_avlb = doc_avlb.copy(update=doc_avlb_update.model_dump(exclude_unset=True))
    await doc_avlb.save()
    return doc_avlb.id
