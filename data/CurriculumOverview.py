from pydantic import BaseModel
from data.CurriculumUnitOverview import CurriculumUnitOverview

class CurriculumOverview(BaseModel):
    title: str
    overview: str
    units: list[CurriculumUnitOverview]