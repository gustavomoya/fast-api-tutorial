from datetime import datetime

from sqlmodel import SQLModel
from pydantic import BaseModel, Field, ConfigDict
from app.users.schemas import UserResponse

class ProjectFilterParams(BaseModel):
    name: str = Field(default=None)
    created_at: datetime = Field(default=None)
    updated_at: datetime = Field(default=None) 
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    
class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime  
    owner: UserResponse  
    
    
class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: str | None = None    
    
class ProjectPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = None    
    
    
class ProjectUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: str | None = None    