from pydantic import BaseModel

class CurriculumUnitOverview(BaseModel):
    id: int
    title: str
    overview: str
    lessons: list[str]
    assignments: list[str]