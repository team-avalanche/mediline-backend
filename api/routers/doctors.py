from fastapi import APIRouter, HTTPException, Depends, Response, status
from api.utils.enum_types import UserType
from api.utils.current_user import GcauDep, Doctor
from api.models.doctors import DoctorProfile, DoctorProfileIn, DoctorAvailability
from api.utils.exceptions import (
    doc_profile_not_found_exc,
    doc_avlb_details_not_found_exc,
)
from beanie import PydanticObjectId


router = APIRouter(prefix="/doctor", tags=["Doctors"])


@router.get("/get-all-doctors")
async def get_all_doctors(user: GcauDep):
    return await DoctorProfile.find_all().to_list()


@router.get("/profile")
async def get_doctor_profile(user: Doctor) -> DoctorProfile:
    doctor = DoctorProfile.find_one(DoctorProfile.id == user.id)
    if not doctor:
        raise doc_profile_not_found_exc
    return doctor


@router.patch("/profile")
async def update_doctor_details(
    profile_details: DoctorProfileIn, user: Doctor
) -> PydanticObjectId:
    doctor = DoctorProfile.find_one(DoctorProfile.id == user.id)
    if not doctor:
        raise doc_profile_not_found_exc
    doctor = doctor.copy(update=profile_details.model_dump(exclude_unset=True))
    await doctor.save()
    return doctor.id


@router.get("/availability")
async def get_doctor_availability(user: Doctor) -> DoctorAvailability:
    doc_avlb = DoctorAvailability.find_one(DoctorAvailability.id == user.id)
    if not doc_avlb:
        raise doc_avlb_details_not_found_exc
    return doc_avlb


@router.patch("/availability")
async def update_doctor_availability(
    doc_avlb_update: DoctorAvailability, user: Doctor
) -> PydanticObjectId:
    doc_avlb = DoctorAvailability.find_one(DoctorProfile.id == user.id)
    if not doc_avlb:
        raise doc_avlb_details_not_found_exc

    doc_avlb = doc_avlb.copy(update=doc_avlb_update.model_dump(exclude_unset=True))
    await doc_avlb.save()
    return doc_avlb.id
