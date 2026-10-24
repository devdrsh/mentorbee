from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BatchBase(BaseModel):
    name: str
    class_number: Optional[str] = None
    class_category: Optional[str] = None
    syllabus: Optional[str] = None
    is_active: bool = True

class BatchCreate(BatchBase):
    pass

class BatchUpdate(BaseModel):
    name: Optional[str] = None
    class_number: Optional[str] = None
    class_category: Optional[str] = None
    syllabus: Optional[str] = None
    is_active: Optional[bool] = None

class BatchResponse(BatchBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
