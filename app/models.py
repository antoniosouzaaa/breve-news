from datetime import datetime, date, timezone
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

def get_utc_now():
    return datetime.now(timezone.utc)

class Edition(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    edition_date: date = Field(unique=True, index=True)
    created_at: datetime = Field(default_factory=get_utc_now)
    email_sent: bool = Field(default=False)

    articles: List["Article"] = Relationship(back_populates="edition")

class Article(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    edition_id: int = Field(foreign_key="edition.id")
    category: str = Field(index=True)  # geral, economia, cultura, design, f1
    title: str
    summary: str
    source_name: str
    source_url: str
    published_at: Optional[str] = None

    edition: Optional[Edition] = Relationship(back_populates="articles")
