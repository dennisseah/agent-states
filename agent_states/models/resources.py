from datetime import datetime, timedelta

import faker
from pydantic import BaseModel, Field


class AvailableDate(BaseModel):
    appt_date: str = Field(description="available appointment date")

    @staticmethod
    def generate_dummy_data(delta: int) -> "AvailableDate":
        return AvailableDate(
            appt_date=(datetime.now() + timedelta(days=delta)).strftime("%Y%m%d")
        )


class AvailableTime(BaseModel):
    appt_time: str = Field(description="available appointment date")

    @staticmethod
    def generate_dummy_data(index: int) -> "AvailableTime":
        return AvailableTime(appt_time=f"{6 + (index + 2)}:00")


class Doctor(BaseModel):
    id: str = Field(..., description="Unique identifier for the doctor")
    name: str = Field(..., description="Name of the doctor")
    available_dates: list[AvailableDate] = Field(
        ...,
        description="List of available appointment dates for the doctor",
    )
    available_times: list[AvailableTime] = Field(
        ...,
        description="List of available appointment times for the doctor",
    )

    @staticmethod
    def generate_dummy_data(department: str) -> "list[Doctor]":
        return [
            Doctor(
                id=f"{department}_{i}",
                name=f"Dr. {faker.Faker().name()}",
                available_dates=[
                    AvailableDate.generate_dummy_data(i) for i in range(1, 6)
                ],
                available_times=[
                    AvailableTime.generate_dummy_data(i) for i in range(1, 6)
                ],
            )
            for i in range(1, 6)
        ]


class Department(BaseModel):
    id: str = Field(..., description="Unique identifier for the department")
    name: str = Field(..., description="Name of the department")
    doctors: list[Doctor] = Field(
        ...,
        description="List of doctors in the department",
    )

    @staticmethod
    def generate_dummy_data(department: str) -> "Department":
        # to simulate an exact match
        return Department(
            id=department.upper()[0:3],
            name=department,
            doctors=Doctor.generate_dummy_data(department),
        )
