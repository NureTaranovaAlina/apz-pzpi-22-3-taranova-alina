# from fastapi import FastAPI, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordRequestForm
# from sqlalchemy.orm import Session
# from app import models, schemas, crud, database
# from app.auth import authenticate_user, create_access_token, get_current_user
#
# app = FastAPI()
#
# models.Base.metadata.create_all(bind=database.engine)
#
#
# @app.post("/register/", response_model=schemas.User)
# def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
#     db_user = crud.get_user_by_username(db, username=user.username)
#     if db_user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Username already registered"
#         )
#     return crud.create_user(db=db, user=user)
#
#
# @app.post("/token/")
# def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
#     user = authenticate_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token = create_access_token(data={"sub": user.username})
#     return {"access_token": access_token, "token_type": "bearer"}
#
#
# @app.post("/flashcards/", response_model=schemas.Flashcard)
# def create_flashcard(
#     flashcard: schemas.FlashcardCreate,
#     db: Session = Depends(database.get_db),
#     current_user: schemas.User = Depends(get_current_user)
# ):
#     return crud.create_flashcard(db=db, flashcard=flashcard, user_id=current_user.id)
#
#
# @app.get("/flashcards/", response_model=list[schemas.Flashcard])
# def read_flashcards(
#     db: Session = Depends(database.get_db),
#     current_user: schemas.User = Depends(get_current_user)
# ):
#     return crud.get_flashcards(db=db, user_id=current_user.id)
#
#
# @app.post("/crosswords/", response_model=schemas.Crossword)
# def create_crossword(
#     crossword: schemas.CrosswordCreate,
#     db: Session = Depends(database.get_db),
#     current_user: schemas.User = Depends(get_current_user)
# ):
#     return crud.create_crossword(db=db, crossword=crossword, user_id=current_user.id)
#
#
# @app.get("/crosswords/", response_model=list[schemas.Crossword])
# def read_crosswords(
#     db: Session = Depends(database.get_db),
#     current_user: schemas.User = Depends(get_current_user)
# ):
#     return crud.get_crosswords(db=db, user_id=current_user.id)
from fastapi import FastAPI
from app import models, database
from app.api.routers import auth, flashcards, crosswords, admin

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

# Подключаем группы маршрутов
app.include_router(auth.router)
app.include_router(flashcards.router)
app.include_router(crosswords.router)
app.include_router(admin.router)
