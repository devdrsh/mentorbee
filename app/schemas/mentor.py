from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MentorLoginRequest(BaseModel):
    name: str  # Mandatory staff name for audit logs
    username: Optional[str] = "mentor"
    assigned_class: Optional[str] = "ALL"  # Universal access for all mentors
    passcode: Optional[str] = None
    password: Optional[str] = None

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
