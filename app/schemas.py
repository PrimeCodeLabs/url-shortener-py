from pydantic import BaseModel, HttpUrl

class URL(BaseModel):
    id: int
    original_url: HttpUrl
    short_url: str

    class Config:
        orm_mode = True
