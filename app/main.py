from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models, crud, schemas
from fastapi.responses import RedirectResponse
import redis

# Initialize Redis
r = redis.Redis(host='cache', port=6379, db=0)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class URL(BaseModel):
    original_url: HttpUrl

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/shorten", response_model=schemas.URL)
def create_short_url(url: URL, db: Session = Depends(get_db)):
    db_url = crud.create_url(db, url.original_url)
    return db_url


@app.get("/{short_url_id}", response_class=RedirectResponse, status_code=301)
def redirect_url(short_url_id: str, db: Session = Depends(get_db)):
    # Check Redis cache first
    cached_url = r.get(short_url_id)
    if cached_url:
        return cached_url.decode("utf-8")
    
    # Fetch from DB if not in cache
    db_url = crud.get_url(db, short_url_id)
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    
    # Store in Redis cache
    r.set(short_url_id, db_url.original_url)
    return db_url.original_url

