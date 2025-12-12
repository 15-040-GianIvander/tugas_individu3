# schemas.py
from pydantic import BaseModel, ConfigDict

class ReviewCreate(BaseModel):
    text: str

class ReviewResponse(BaseModel):
    id: int
    text: str
    sentiment: str | None = None
    key_points: str | None = None

    model_config = ConfigDict(from_attributes=True)
