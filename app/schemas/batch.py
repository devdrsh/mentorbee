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

class BatchUpdate(BatchBase):
    pass

class BatchResponse(BatchBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
