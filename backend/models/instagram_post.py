from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

class InstagramPostBase(BaseModel):
    image: str
    likes: int = 0
    comments: int = 0
    postUrl: Optional[str] = None

class InstagramPostCreate(InstagramPostBase):
    pass

class InstagramPost(InstagramPostBase):
    id: str = Field(alias="_id")
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
