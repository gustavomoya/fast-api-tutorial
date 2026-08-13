from datetime import datetime

from sqlmodel import SQLModel


class UserResponse(SQLModel):
    id: int
    name: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    # model_config = {
    #     "from_attributes": True
    # }
