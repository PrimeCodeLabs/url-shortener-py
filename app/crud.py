from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas
import hashlib

def generate_short_url(id: int) -> str:
    hash_object = hashlib.sha256(str(id).encode())
    hash_hex = hash_object.hexdigest()
    return hash_hex[:6]

def create_url(db: Session, original_url: str) -> schemas.URL:
    original_url_str = str(original_url)  # Convert URL to string
    for _ in range(3):  # Try 3 times to avoid collisions
        short_url = generate_short_url(id)
        db_url = models.URL(original_url=original_url_str, short_url=short_url)
        db.add(db_url)
        try:
            db.commit()
            db.refresh(db_url)
            return db_url
        except IntegrityError:
            db.rollback()
    raise HTTPException(status_code=500, detail="Could not create short URL after 3 attempts")

def get_url(db: Session, short_url: str) -> models.URL:
    return db.query(models.URL).filter(models.URL.short_url == short_url).first()
