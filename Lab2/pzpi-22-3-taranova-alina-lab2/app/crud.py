from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext
import math
from collections import Counter
from datetime import date, timedelta


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_flashcard(db: Session, flashcard: schemas.FlashcardCreate, user_id: int):
    db_flashcard = models.Flashcard(**flashcard.dict(), owner_id=user_id)
    db.add(db_flashcard)
    db.commit()
    db.refresh(db_flashcard)
    return db_flashcard


def get_flashcards(db: Session, user_id: int):
    return db.query(models.Flashcard).filter(models.Flashcard.owner_id == user_id).all()


def create_crossword(db: Session, crossword: schemas.CrosswordCreate, user_id: int):
    db_crossword = models.Crossword(**crossword.dict(), owner_id=user_id)
    db.add(db_crossword)
    db.commit()
    db.refresh(db_crossword)
    return db_crossword


def get_crosswords(db: Session, user_id: int):
    return db.query(models.Crossword).filter(models.Crossword.owner_id == user_id).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def compute_tag_idf(db: Session, user_id: int) -> dict[str, float]:

    cards = db.query(models.Flashcard).filter_by(owner_id=user_id).all()
    N = len(cards) or 1
    counter: Counter[str] = Counter(tag for c in cards for tag in (c.tags or []))
    return {tag: math.log(N / df) for tag, df in counter.items()}

def compute_retention(db: Session, user_id: int) -> list[dict]:

    cards = db.query(models.Flashcard).filter_by(owner_id=user_id).all()
    today = date.today()
    result = []
    for c in cards:
        hl = max(1.0, (c.ef or 2.5) * max(c.interval or 1, 1))
        t = (today - (c.next_review or today)).days
        P = math.exp(-t / hl)
        result.append({
            "id": c.id,
            "word": c.word,
            "retention": round(P, 3)
        })
    return result

def get_admin_report(db: Session) -> dict:

    total_users = db.query(models.User).count()
    total_flashcards = db.query(models.Flashcard).count()
    avg = round(total_flashcards / max(1, total_users), 2)
    return {
        "total_users": total_users,
        "total_flashcards": total_flashcards,
        "avg_flashcards_per_user": avg,
    }
def _sm2(card: models.Flashcard, quality: int):
    # ease factor
    EF = card.ef or 2.5
    EF = max(1.3, EF + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
    # интервал
    if card.repetitions == 0:
        interval = 1
    elif card.repetitions == 1:
        interval = 6
    else:
        interval = int(card.interval * EF)
    card.ef = EF
    card.interval = interval
    card.repetitions += 1
    card.next_review = date.today() + timedelta(days=interval)

def review_flashcard(db: Session, flashcard_id: int, quality: int):

    card = db.query(models.Flashcard).filter(models.Flashcard.id == flashcard_id).first()
    if not card:
        return None
    _sm2(card, quality)
    db.commit()
    db.refresh(card)
    return card
