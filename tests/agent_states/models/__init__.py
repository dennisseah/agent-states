from agent_states.models.appointment import Appointment


def test_init():
    appointment = Appointment(
        department_id="cardiology",
        doctor_id="dr_smith",
        appointment_date="2023-10-01",
        appointment_time="10:00 AM",
    )
    assert appointment.department_id == "cardiology"
    assert appointment.doctor_id == "dr_smith"
    assert appointment.appointment_date == "2023-10-01"
    assert appointment.appointment_time == "10:00 AM"
