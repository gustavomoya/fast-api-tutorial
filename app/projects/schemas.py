from datetime import datetime

from sqlmodel import SQLModel
from pydantic import BaseModel, Field
from app.users.schemas import UserResponse

class ProjectFilterParams(BaseModel):
    name: str = Field(default=None)
    created_at: datetime = Field(default=None)
    updated_at: datetime = Field(default=None) 
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    
class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime  
    owner: UserResponse  