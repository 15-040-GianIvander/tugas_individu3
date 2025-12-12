# models.py
from sqlalchemy import Column, Integer, String
from database import Base

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    sentiment = Column(String, nullable=True)
    key_points = Column(String, nullable=True)
