from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId

class AdminLogin(BaseModel):
    username: str
    password: str

class AdminToken(BaseModel):
    token: str
    username: str
    expiresAt: datetime

class Admin(BaseModel):
    id: str = Field(alias="_id")
    username: str
    passwordHash: str
    createdAt: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
