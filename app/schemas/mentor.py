from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MentorLoginRequest(BaseModel):
    name: str
    assigned_class: str  # "8TH", "9TH", "10TH", "11TH SCI", "11TH COM", "12TH SCI", "12TH COM", "ALL"
    passcode: str

class MentorTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    name: str
    assigned_class: str

class MentorActionLogRequest(BaseModel):
    action: str  # "VIEW_DASHBOARD", "COPY_MESSAGE", "COPY_LINK", "JOIN_ZOOM"
    session_id: Optional[int] = None
    batch_name: Optional[str] = None
    details: Optional[str] = None

class MentorAccessLogResponse(BaseModel):
    id: int
    mentor_name: str
    assigned_class: str
    session_id: Optional[int] = None
    batch_name: Optional[str] = None
    action: str
    ip_address: Optional[str] = None
    details: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
