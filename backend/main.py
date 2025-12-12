# main.py
import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Review
from schemas import ReviewCreate, ReviewResponse
from services.sentiment import analyze_sentiment
from services.keypoints import extract_keypoints
from fastapi.middleware.cors import CORSMiddleware

# logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("product-review-app")

# create tables if not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Product Review Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/analyze-review", response_model=ReviewResponse)
async def analyze_review(review: ReviewCreate, db: Session = Depends(get_db)):
    logger.info("Analyze request received")
    # 1) sentiment (async)
    try:
        sentiment = await analyze_sentiment(review.text)
    except Exception as e:
        logger.exception("Sentiment analysis failed - using fallback 'unknown'")
        sentiment = "unknown"

    # 2) keypoints (sync)
    try:
        key_points = extract_keypoints(review.text)
    except Exception as e:
        logger.exception("Keypoint extraction failed - using fallback")
        key_points = "keypoint_extraction_failed"

    # 3) save to DB
    try:
        db_review = Review(text=review.text, sentiment=sentiment, key_points=key_points)
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        logger.info("Saved review id=%s", db_review.id)
        return db_review
    except Exception as e:
        logger.exception("Database save failed")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reviews", response_model=list[ReviewResponse])
def get_reviews(db: Session = Depends(get_db)):
    items = db.query(Review).order_by(Review.id.desc()).all()
    return items

@app.get("/health")
def health():
    return {"status": "ok"}
