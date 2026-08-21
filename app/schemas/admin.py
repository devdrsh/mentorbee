from pydantic import BaseModel, EmailStr
from datetime import datetime

class AdminBase(BaseModel):
    name: str
    email: EmailStr
    role: str = "COORDINATOR"
    assigned_classes: str = "ALL"
    is_active: bool = True

class AdminCreate(AdminBase):
    password: str

class AdminResponse(AdminBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class AdminLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    name: str
    role: str
    assigned_classes: str
