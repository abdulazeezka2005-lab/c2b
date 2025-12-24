from fastapi import APIRouter, HTTPException, Depends
from models.review import Review, ReviewCreate
from routes.admin import verify_token
from datetime import datetime
import os
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

router = APIRouter(prefix="/reviews", tags=["reviews"])

def get_database():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    return client[os.environ['DB_NAME']]

@router.post("", response_model=dict)
async def create_review(review: ReviewCreate):
    try:
        db = get_database()
        
        # Validate rating
        if review.rating < 1 or review.rating > 5:
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
        
        review_dict = review.dict()
        review_dict["approved"] = False  # Requires admin approval
        review_dict["createdAt"] = datetime.utcnow()
        
        result = await db.reviews.insert_one(review_dict)
        review_dict["_id"] = str(result.inserted_id)
        
        return {"review": review_dict, "message": "Review submitted for approval"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/product/{product_id}", response_model=dict)
async def get_product_reviews(product_id: str):
    try:
        db = get_database()
        
        # Only return approved reviews for public
        reviews = await db.reviews.find({
            "productId": product_id,
            "approved": True
        }).to_list(100)
        
        for review in reviews:
            review["_id"] = str(review["_id"])
        
        # Calculate average rating
        avg_rating = sum(r["rating"] for r in reviews) / len(reviews) if reviews else 0
        
        return {
            "reviews": reviews,
            "count": len(reviews),
            "averageRating": round(avg_rating, 1)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/pending", response_model=dict)
async def get_pending_reviews(username: str = Depends(verify_token)):
    """Admin only - get pending reviews"""
    try:
        db = get_database()
        
        reviews = await db.reviews.find({"approved": False}).to_list(100)
        
        for review in reviews:
            review["_id"] = str(review["_id"])
        
        return {"reviews": reviews, "count": len(reviews)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{review_id}/approve", response_model=dict)
async def approve_review(review_id: str, username: str = Depends(verify_token)):
    """Admin only - approve a review"""
    try:
        db = get_database()
        
        if not ObjectId.is_valid(review_id):
            raise HTTPException(status_code=400, detail="Invalid review ID")
        
        result = await db.reviews.update_one(
            {"_id": ObjectId(review_id)},
            {"$set": {"approved": True}}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Review not found")
        
        return {"message": "Review approved successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{review_id}", response_model=dict)
async def delete_review(review_id: str, username: str = Depends(verify_token)):
    """Admin only - delete a review"""
    try:
        db = get_database()
        
        if not ObjectId.is_valid(review_id):
            raise HTTPException(status_code=400, detail="Invalid review ID")
        
        result = await db.reviews.delete_one({"_id": ObjectId(review_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Review not found")
        
        return {"message": "Review deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
