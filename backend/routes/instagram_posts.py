from fastapi import APIRouter, HTTPException
from models.instagram_post import InstagramPost, InstagramPostCreate
from datetime import datetime
import os
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter(prefix="/instagram-posts", tags=["instagram"])

def get_database():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    return client[os.environ['DB_NAME']]

@router.get("", response_model=dict)
async def get_instagram_posts():
    try:
        db = get_database()
        posts = await db.instagram_posts.find().to_list(1000)
        
        # Convert ObjectId to string
        for post in posts:
            post["_id"] = str(post["_id"])
        
        return {"posts": posts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("", response_model=dict)
async def create_instagram_post(post: InstagramPostCreate):
    try:
        db = get_database()
        post_dict = post.dict()
        post_dict["createdAt"] = datetime.utcnow()
        
        result = await db.instagram_posts.insert_one(post_dict)
        post_dict["_id"] = str(result.inserted_id)
        
        return {"post": post_dict, "message": "Post created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
