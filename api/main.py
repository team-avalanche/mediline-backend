from api.app import app
from api.routers import appointments, auth, doctors, patients, register, user

app.include_router(auth.router)
app.include_router(register.router)
app.include_router(user.router)
app.include_router(patients.router)
app.include_router(doctors.router)
app.include_router(appointments.router)
