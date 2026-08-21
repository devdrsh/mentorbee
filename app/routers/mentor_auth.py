from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

from app.database import get_db
from app.models.mentor import MentorUser, MentorAccessLog
from app.schemas.mentor import MentorLoginRequest, MentorTokenResponse, MentorActionLogRequest
from app.config import settings

router = APIRouter(prefix="/api/mentor", tags=["mentor_auth"])

STAFF_PASSCODE = "AGENTBEE0809"

CLASS_PASSCODES = {
    "8TH": ["AGENTBEE0809", "MENTOR8TH", "BEE8TH"],
    "9TH": ["AGENTBEE0809", "MENTOR9TH", "BEE9TH"],
    "10TH": ["AGENTBEE0809", "MENTOR10TH", "BEE10TH"],
    "11TH SCI": ["AGENTBEE0809", "MENTOR11SCI", "BEE11SCI"],
    "11TH COM": ["AGENTBEE0809", "MENTOR11COM", "BEE11COM"],
    "12TH SCI": ["AGENTBEE0809", "MENTOR12SCI", "BEE12SCI"],
    "12TH COM": ["AGENTBEE0809", "MENTOR12COM", "BEE12COM"],
    "ALL": ["AGENTBEE0809", "MENTORALL", "BEEALL"]
}

def create_mentor_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire, "type": "mentor"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def get_current_mentor(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Mentor authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "mentor":
            raise HTTPException(status_code=401, detail="Invalid token type")
        name = payload.get("sub")
        assigned_class = payload.get("assigned_class")
        if not name or not assigned_class:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return {"name": name, "assigned_class": assigned_class}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@router.post("/login", response_model=MentorTokenResponse)
def mentor_login(login_data: MentorLoginRequest, request: Request, db: Session = Depends(get_db)):
    assigned_class = login_data.assigned_class.strip().upper()
    passcode_input = login_data.passcode.strip()
    
    # Verify passcode (either master passcode or class-specific passcode)
    allowed_passcodes = CLASS_PASSCODES.get(assigned_class, [STAFF_PASSCODE])
    if passcode_input != STAFF_PASSCODE and passcode_input.upper() not in allowed_passcodes:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid verification passcode for {assigned_class}. Please enter the correct staff passcode."
        )
    
    name = login_data.name.strip().upper()
    assigned_class = login_data.assigned_class.strip().upper()
    client_ip = request.client.host if request.client else "unknown"

    # Find or create mentor user record
    mentor = db.query(MentorUser).filter(MentorUser.name == name).first()
    if not mentor:
        mentor = MentorUser(
            name=name,
            assigned_class=assigned_class,
            is_active=True
        )
        db.add(mentor)
    else:
        mentor.assigned_class = assigned_class
        mentor.last_login_at = datetime.utcnow()
    
    # Record Login Audit Log
    log = MentorAccessLog(
        mentor_name=name,
        assigned_class=assigned_class,
        action="LOGIN",
        ip_address=client_ip,
        details=f"Staff logged in for class {assigned_class}"
    )
    db.add(log)
    db.commit()

    token = create_mentor_token(
        data={"sub": name, "assigned_class": assigned_class}
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "name": name,
        "assigned_class": assigned_class
    }

@router.post("/log-action")
def log_mentor_action(log_data: MentorActionLogRequest, request: Request, db: Session = Depends(get_db), current_mentor: dict = Depends(get_current_mentor)):
    client_ip = request.client.host if request.client else "unknown"
    log = MentorAccessLog(
        mentor_name=current_mentor["name"],
        assigned_class=current_mentor["assigned_class"],
        session_id=log_data.session_id,
        batch_name=log_data.batch_name,
        action=log_data.action,
        ip_address=client_ip,
        details=log_data.details
    )
    db.add(log)
    db.commit()
    return {"status": "success"}

@router.get("/me")
def get_mentor_profile(current_mentor: dict = Depends(get_current_mentor)):
    return current_mentor
