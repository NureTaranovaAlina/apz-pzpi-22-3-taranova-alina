from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import date

class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    role: str

    class Config:
        orm_mode = True


class FlashcardBase(BaseModel):
    word: str
    translation: str
    definition: Optional[str] = None
    examples: Optional[List[str]] = None
    tags: Optional[List[str]] = None
class FlashcardCreate(FlashcardBase):
    pass


class Flashcard(FlashcardBase):
    id: int
    owner_id: int
    ef: float
    interval: int
    repetitions: int
    next_review: Optional[date] = None

    class Config:
        orm_mode = True

class TagIDF(BaseModel):
    tag: str
    idf: float

class FlashcardRetention(BaseModel):
    id: int
    word: str
    retention: float  # [0..1]

class AdminReport(BaseModel):
    total_users: int
    total_flashcards: int
    avg_flashcards_per_user: float
class CrosswordBase(BaseModel):
    title: str
    grid: List[List[str]]
    clues: Dict[str, Dict[str, str]]


class CrosswordCreate(CrosswordBase):
    pass


class Crossword(CrosswordBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
class ReviewRequest(BaseModel):
    quality: int = Field(
        ...,
        ge=0, le=5,
        description="Response quality assessment from 0 (don't remember at all) to 5 (easy)"
    )