
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    role: str

class LessonCreate(BaseModel):
    title: str
    content: str

class BlogCreate(BaseModel):
    title: str
    content: str
    author: str

class TestCreate(BaseModel):
    question: str
    options: str
    correct_answer: str

class AnswerCreate(BaseModel):
    test_id: int
    selected_option: str
