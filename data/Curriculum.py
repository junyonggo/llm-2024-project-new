from pydantic import BaseModel
from data.CurriculumUnit import CurriculumUnit

class Curriculum(BaseModel):
    title: str
    overview: str
    units: list[CurriculumUnit]