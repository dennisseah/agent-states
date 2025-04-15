from typing import Any

from langchain_core.tools import tool

from agent_states.data.builder import departments
from agent_states.models.appointment import Appointment
from agent_states.models.resources import Doctor


@tool
def get_department_names() -> list[dict[str, str]]:
    """
    Get the departments from the database.
    """
    depts = [d.model_dump() for d in departments]
    for dept in depts:
        del dept["doctors"]
    return depts


@tool(return_direct=True)
def get_doctors(
    department_id: str,
    doctor_id: str | None,
    appointment_date: str | None,
    appointment_time: str | None,
) -> dict[str, Any]:
    """
    Get the doctors in a department.

    :param department_id: The ID of the department.
    :return: A list of doctors in the department.
    """
    depts = [d for d in departments if d.id == department_id]
    choices = []
    if depts:
        dept = depts[0]
        doctors = [d.model_dump() for d in dept.doctors]
        for doctor in doctors:
            del doctor["available_dates"]
            del doctor["available_times"]
        choices = doctors

    return {
        "label": "Select a doctor",
        "choices": choices,
        "state": generate_output(
            department_id=department_id,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
        ),
    }


def find_doctor(department_id: str, doctor_id: str) -> Doctor | None:
    depts = [d for d in departments if d.id == department_id]
    if depts:
        dept = depts[0]
        for doc in dept.doctors:
            if doc.id == doctor_id:
                return doc
    return None


@tool(return_direct=True)
def get_available_dates_of_doctor(
    department_id: str,
    doctor_id: str,
    appointment_date: str | None,
    appointment_time: str | None,
) -> dict[str, Any]:
    """
    Get the available dates for a doctor.

    :param doctor_id: The ID of the doctor.
    :return: A list of available dates for the doctor.
    """
    doctor = find_doctor(department_id, doctor_id)
    choices = [d.appt_date for d in doctor.available_dates] if doctor else []

    return {
        "label": "Select a date for your appointment",
        "choices": choices,
        "state": generate_output(
            department_id=department_id,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
        ),
    }


@tool(return_direct=True)
def get_available_times_of_doctor(
    department_id: str,
    doctor_id: str,
    appointment_date: str | None,
    appointment_time: str | None,
) -> dict[str, Any]:
    """
    Get the available times for a doctor.

    :param doctor_id: The ID of the doctor.
    :return: A list of available times for the doctor.
    """
    doctor = find_doctor(department_id, doctor_id)
    choices = [d.appt_time for d in doctor.available_times] if doctor else []

    return {
        "label": "Select a time for your appointment",
        "choices": choices,
        "state": generate_output(
            department_id=department_id,
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
        ),
    }


def generate_output(
    department_id: str,
    doctor_id: str | None,
    appointment_date: str | None,
    appointment_time: str | None,
) -> dict[str, str]:
    """
    Generate the output for the appointment.

    :param department_id: The ID of the department.
    :param doctor_id: The ID of the doctor.
    :param appointment_date: The date of the appointment.
    :param appointment_time: The time of the appointment.
    :return: A dictionary with the appointment information.
    """
    return Appointment(
        department_id=department_id,
        doctor_id=doctor_id,
        appointment_date=appointment_date,
        appointment_time=appointment_time,
    ).model_dump()


@tool()
def capture_state(
    department_id: str,
    doctor_id: str | None,
    appointment_date: str | None,
    appointment_time: str | None,
) -> dict[str, str]:
    """
    Generate the output for the appointment.

    :param department_id: The ID of the department.
    :param doctor_id: The ID of the doctor.
    :param appointment_date: The date of the appointment.
    :param appointment_time: The time of the appointment.
    :return: A dictionary with the appointment information.
    """
    return generate_output(
        department_id=department_id,
        doctor_id=doctor_id,
        appointment_date=appointment_date,
        appointment_time=appointment_time,
    )
