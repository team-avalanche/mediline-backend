from beanie import PydanticObjectId
from fastapi import APIRouter

from api.models.appointments import Appointment, AppointmentIn
from api.utils.current_user import ActiveUser, Patient
from api.utils.enum_types import AppointmentStatus, UserType
from api.utils.exceptions import invalid_cancellation_request

router = APIRouter(prefix="/appointment", tags=["Appointments"])


# both patient and doctor can call this endpoint
@router.get("/get-all-appointments")
async def get_all_appointments(user: ActiveUser) -> Appointment:
    # TODO: filter by date
    if user.user_type == UserType.doctor:
        return await Appointment.find(Appointment.doctor_id == user.id).to_list()
    else:
        return await Appointment.find(Appointment.patient_id == user.id).to_list()


# only patient can book an appointment
@router.post("/new-appointment")
async def request_new_appointment(aptnmnt_in: AppointmentIn, user: Patient):
    aptnmnt = Appointment(
        **aptnmnt_in.model_dump(),
        patient_id=user.id,
        status=AppointmentStatus.scheduled
    )
    await aptnmnt.insert()
    return aptnmnt.id


# either patient or doctor can cancel an appointment
@router.post("/cancel-appointment")
async def cancel_appointment(aptnmnt_id: PydanticObjectId, user: ActiveUser):
    aptmnt: Appointment = await Appointment.find_one(id == aptnmnt_id)
    if aptmnt.doctor_id == user.id or aptmnt.patient_id == user.id:
        aptmnt.status = AppointmentStatus.cancelled
        await aptmnt.save()
        return aptmnt.id
    raise invalid_cancellation_request
