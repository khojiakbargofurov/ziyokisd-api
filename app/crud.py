
from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_lesson(db: Session, lesson: schemas.LessonCreate):
    db_lesson = models.Lesson(**lesson.dict())
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

def get_lessons(db: Session):
    return db.query(models.Lesson).all()

def create_blog(db: Session, blog: schemas.BlogCreate):
    db_blog = models.Blog(**blog.dict())
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def get_blogs(db: Session):
    return db.query(models.Blog).all()

def create_test(db: Session, test: schemas.TestCreate):
    db_test = models.Test(**test.dict())
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test

def get_tests(db: Session):
    return db.query(models.Test).all()

def answer_test(db: Session, answer: schemas.AnswerCreate, user_id: int):
    test = db.query(models.Test).filter(models.Test.id == answer.test_id).first()
    is_correct = test.correct_answer == answer.selected_option
    db_answer = models.UserAnswer(user_id=user_id, test_id=answer.test_id,
                                  selected_option=answer.selected_option, is_correct=is_correct)
    db.add(db_answer)
    db.commit()
    return db_answer
