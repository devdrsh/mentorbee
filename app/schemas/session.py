from pydantic import BaseModel
from typing import Optional
from datetime import date, time, datetime
from app.schemas.batch import BatchResponse

class ClassSessionBase(BaseModel):
    batch_id: int
    class_category: Optional[str] = None
    topic: str
    class_date: date
    start_time: time
    zoom_link: str
    meeting_id: str
    passcode: str
    is_active: bool = True

class ClassSessionCreate(ClassSessionBase):
    pass

class ClassSessionUpdate(ClassSessionBase):
    pass

class ClassSessionResponse(ClassSessionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int]
    updated_by: Optional[int]
    formatted_message: Optional[str] = None
    
    # We can also optionally include batch info
    batch: Optional['BatchResponse'] = None

    class Config:
        from_attributes = True
