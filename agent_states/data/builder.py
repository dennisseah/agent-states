from agent_states.models.resources import Department

DEPARTMENT_NAMES = [
    "Cardiology",
    "Neurology",
    "Orthopedics",
    "Dermatology",
    "Pediatrics",
    "Oncology",
    "Endocrinology",
    "Gastroenterology",
]

departments = [Department.generate_dummy_data(name) for name in DEPARTMENT_NAMES]
