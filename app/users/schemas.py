from datetime import datetime

from sqlmodel import SQLModel
from pydantic import BaseModel, Field


class UserResponse(SQLModel):
    id: int
    name: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    
class UserFilterParams(BaseModel):
    name: str = Field(default=None)
    email: str = Field(default=None)
    is_active: bool = Field(default=None)
    created_at: datetime = Field(default=None)
    updated_at: datetime = Field(default=None) 
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
