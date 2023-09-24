from fastapi import HTTPException, status

user_not_active = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="User Account is not activated."
)

doc_profile_not_found_exc = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Doctor Profile Not Found"
)
patient_profile_not_found_exc = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Patient Profile Not Found"
)

doc_avlb_details_not_found_exc = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Doctor Availability Details Not Found",
)

method_not_allowed_for_doctor = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="The method you are trying to access is only for patient users.",
)

method_not_allowed_for_patient = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="The method you are trying to access is only for doctor users.",
)


invalid_cancellation_request = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Cant cancel appointment",
)
