from agent_states.models.resources import Department


def test_department_init():
    department = Department.generate_dummy_data("Cardiology")

    assert department.id == "CAR"
    assert department.name == "Cardiology"
    assert len(department.doctors) == 5
