from pydantic import BaseModel
from data.Question import Question

class Lesson(BaseModel):
    title: str
    paragraphs: list[str]
    quiz: list[Question]