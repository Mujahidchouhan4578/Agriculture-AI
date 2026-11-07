from typing import TypedDict

class MAHSOULState(TypedDict):

    pdf_path: str

    crop: str

    area: float

    area_unit: str

    pdf_text: str

    soil_data: dict

    crop_requirements: dict

    fertilizer_plan: dict

    calculation_result: dict

    advisory: str