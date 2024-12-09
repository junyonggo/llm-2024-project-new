from pydantic import BaseModel

class Question(BaseModel):
    id: int
    sentence: str
    possible_answers: list[str]
    correct_answer: str
