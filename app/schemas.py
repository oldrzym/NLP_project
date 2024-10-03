from pydantic import BaseModel, Field
from typing import Dict

class MaskRequestModel(BaseModel):
    text: str = Field(..., example="Кузьмин Сергей родился 15.08.1990, но в свидетельстве о рождении, выданным в ЗАГСе, написали, что 15.07.1990.")

class MaskResponseModel(BaseModel):
    text: str = Field(..., example="Кузьмин Сергей родился 15.08.1990, но в свидетельстве о рождении, выданным в ЗАГСе, написали, что 15.07.1990.")
    masked_text: str = Field(..., example="{NAME_1} родился {DATE_1}, но в свидетельстве о рождении, выданным в {ORGANIZATION_1}, написали, что {DATE_2}.")
    masks_dict: Dict[str, str] = Field(..., example={
        "{NAME_1}": "Кузьмин Сергей", 
        "{DATE_1}": "15.08.1990",
        "{DATE_2}": "15.07.1990",
        "{ORGANIZATION_1}": "ЗАГСе"
    })
