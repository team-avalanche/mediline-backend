from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter
from pydantic import ValidationError

from api.models.doctors import (
    DoctorAvailability,
    DoctorAvailabilityInSchema,
    DoctorProfile,
    DoctorProfileIn,
)
from api.utils.current_user import ActiveUser, Doctor
from api.utils.exceptions import (
    doc_avlb_details_not_found_exc,
    doc_profile_not_found_exc,
    invalid_doc_avlb_details_exc,
)

router = APIRouter(prefix="/doctor", tags=["Doctors"])


@router.get("/get-all-doctors")
async def get_all_doctors(user: ActiveUser) -> List[DoctorProfile]:
    return await DoctorProfile.find_all().to_list()


@router.get("/get-doctor-profile")
async def get_doctor_profile(
    doctor_id: PydanticObjectId, user: ActiveUser
) -> DoctorProfile:
    doctor_profile = await DoctorProfile.find_one(DoctorProfile.id == doctor_id)
    if not doctor_profile:
        raise doc_profile_not_found_exc
    return doctor_profile


@router.get("/get-doctor-availability")
async def get_doctor_availability(
    doctor_id: PydanticObjectId, user: ActiveUser
) -> DoctorAvailability:
    doc_avlb = await DoctorAvailability.find_one(DoctorProfile.id == doctor_id)
    if not doc_avlb:
        raise doc_avlb_details_not_found_exc
    return doc_avlb


@router.get("/my-profile")
async def get_doctor_self_profile(user: Doctor) -> DoctorProfile:
    doctor = await DoctorProfile.find_one(DoctorProfile.id == user.id)
    if not doctor:
        raise doc_profile_not_found_exc
    return doctor


@router.patch("/my-profile")
async def update_doctor_self_profile(
    profile_details: DoctorProfileIn, user: Doctor
) -> PydanticObjectId:
    doctor = await DoctorProfile.find_one(DoctorProfile.id == user.id)
    if not doctor:
        raise doc_profile_not_found_exc
    doctor = doctor.model_copy(update=profile_details.model_dump(exclude_unset=True))
    await doctor.save()
    return doctor.id


@router.get("/my-availability")
async def get_doctor_self_availability(user: Doctor) -> DoctorAvailability:
    doc_avlb = await DoctorAvailability.find_one(DoctorAvailability.id == user.id)
    if not doc_avlb:
        raise doc_avlb_details_not_found_exc
    return doc_avlb


@router.patch("/my-availability")
async def update_doctor_self_availability(
    doc_avlb_update: DoctorAvailabilityInSchema, user: Doctor
) -> PydanticObjectId:
    doc_avlb = await DoctorAvailability.find_one(DoctorAvailability.id == user.id)
    if not doc_avlb:
        raise doc_avlb_details_not_found_exc

    # validate data types of update
    try:
        DoctorAvailabilityInSchema(**doc_avlb_update.model_dump())
    except ValidationError as e:
        print(e)
        raise invalid_doc_avlb_details_exc(str(e))

    # typecasting
    # for the api we are accepting data and validating with int as dict keys
    # but int keys are invalid in bson document/mongo db... they need to stored as str
    # so typecasting the doctor_availability dict
    doc_avlb.doctor_availability = DoctorAvailability(
        id=doc_avlb.id, doctor_availability=doc_avlb_update.doctor_availability
    ).doctor_availability
    # the above code doesnt do what i expected it to do
    # but i am keeping this, to fix later, and reminder of what i want

    await doc_avlb.save()
    return doc_avlb.id
