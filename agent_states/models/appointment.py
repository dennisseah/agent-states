from pydantic import BaseModel


class Appointment(BaseModel):
    department_id: str
    doctor_id: str | None = None
    appointment_date: str | None = None
    appointment_time: str | None = None
