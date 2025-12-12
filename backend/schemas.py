# schemas.py
from pydantic import BaseModel

class ReviewCreate(BaseModel):
    text: str

class ReviewResponse(BaseModel):
    id: int
    text: str
    sentiment: str | None = None
    key_points: str | None = None

    class Config:
        orm_mode = True
        # NOTE: if you're on pydantic v2, change to: from_attributes = True
        # See pydantic docs if needed.
