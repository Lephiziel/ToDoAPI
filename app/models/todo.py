from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(..., max_length=1000)

class TodoUpdate(BaseModel):
    title: str = Field(..., min_length=1)
    description: str | None = Field(...)
    is_completed: bool = Field(...)

class TodoResponse(BaseModel):
    id: int
    title: str
    description: str | None
    is_completed: bool
    created_at: datetime
    updated_at: datetime
    owner_id: int

    model_config = ConfigDict(from_attributes=True)