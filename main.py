
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, schemas, crud, auth, database

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()

@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    return crud.create_user(db, user)

@app.post("/token")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = crud.get_user_by_username(db, form.username)
    if not user or not auth.pwd_context.verify(form.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Login xato")
    token = auth.create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/lessons/", dependencies=[Depends(auth.require_role("admin"))])
def add_lesson(lesson: schemas.LessonCreate, db: Session = Depends(database.get_db)):
    return crud.create_lesson(db, lesson)

@app.get("/lessons/")
def get_lessons(db: Session = Depends(database.get_db)):
    return crud.get_lessons(db)

@app.post("/blogs/", dependencies=[Depends(auth.require_role("admin"))])
def add_blog(blog: schemas.BlogCreate, db: Session = Depends(database.get_db)):
    return crud.create_blog(db, blog)

@app.get("/blogs/")
def get_blogs(db: Session = Depends(database.get_db)):
    return crud.get_blogs(db)

@app.post("/tests/", dependencies=[Depends(auth.require_role("admin"))])
def add_test(test: schemas.TestCreate, db: Session = Depends(database.get_db)):
    return crud.create_test(db, test)

@app.get("/tests/")
def get_tests(db: Session = Depends(database.get_db)):
    return crud.get_tests(db)

@app.post("/tests/answer")
def answer_test(answer: schemas.AnswerCreate,
                user=Depends(auth.require_role("user")),
                db: Session = Depends(database.get_db)):
    return crud.answer_test(db, answer, user.id)
