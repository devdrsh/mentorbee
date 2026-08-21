from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, List
from jose import JWTError, jwt
import bcrypt

from app.database import get_db
from app.models.admin import AdminUser
from app.models.mentor import MentorAccessLog, MentorUser
from app.schemas.admin import AdminLogin, Token, AdminResponse
from app.schemas.mentor import MentorAccessLogResponse
from app.config import settings

router = APIRouter(prefix="/api/admin", tags=["admin"])

def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=12)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

@router.post("/login", response_model=Token)
def login(login_data: AdminLogin, db: Session = Depends(get_db)):
    admin = db.query(AdminUser).filter(AdminUser.email == login_data.email).first()
    if not admin or not verify_password(login_data.password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not admin.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": admin.email,
            "name": admin.name,
            "role": admin.role or "COORDINATOR",
            "assigned_classes": admin.assigned_classes or "ALL"
        },
        expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "name": admin.name,
        "role": admin.role or "COORDINATOR",
        "assigned_classes": admin.assigned_classes or "ALL"
    }

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/admin/login")

def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    admin = db.query(AdminUser).filter(AdminUser.email == email).first()
    if admin is None:
        raise credentials_exception
    if not admin.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return admin

@router.get("/me")
def get_me(current_admin: AdminUser = Depends(get_current_admin)):
    return {
        "id": current_admin.id,
        "name": current_admin.name,
        "email": current_admin.email,
        "role": current_admin.role,
        "assigned_classes": current_admin.assigned_classes
    }

@router.get("/audit-logs", response_model=List[MentorAccessLogResponse])
def get_audit_logs(
    action: Optional[str] = Query(None),
    assigned_class: Optional[str] = Query(None),
    limit: int = Query(100, le=500),
    db: Session = Depends(get_db),
    current_admin: AdminUser = Depends(get_current_admin)
):
    if current_admin.role != "SUPER_ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Only Super Admin can view audit logs."
        )
    query = db.query(MentorAccessLog)
    if action:
        query = query.filter(MentorAccessLog.action == action.upper())
    if assigned_class and assigned_class != "ALL":
        query = query.filter(MentorAccessLog.assigned_class == assigned_class)
    return query.order_by(MentorAccessLog.created_at.desc()).limit(limit).all()

@router.get("/coordinators")
def get_coordinators(db: Session = Depends(get_db), current_admin: AdminUser = Depends(get_current_admin)):
    coordinators = db.query(AdminUser).filter(AdminUser.is_active == True).all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "email": c.email,
            "role": c.role,
            "assigned_classes": c.assigned_classes
        }
        for c in coordinators
    ]
