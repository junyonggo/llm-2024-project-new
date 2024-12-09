from pydantic import BaseModel
from data.Lesson import Lesson

class CurriculumUnit(BaseModel):
    id: int
    title: str
    overview: str
    lessons: list[Lesson]