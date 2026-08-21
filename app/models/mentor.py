from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.database import Base

class MentorUser(Base):
    __tablename__ = "mentor_users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    assigned_class = Column(String, nullable=False)  # "8TH", "9TH", "10TH", "11TH SCI", "11TH COM", "12TH SCI", "12TH COM", "ALL"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class MentorAccessLog(Base):
    __tablename__ = "mentor_access_logs"
    id = Column(Integer, primary_key=True, index=True)
    mentor_name = Column(String, nullable=False, index=True)
    assigned_class = Column(String, nullable=False)
    session_id = Column(Integer, nullable=True)
    batch_name = Column(String, nullable=True)
    action = Column(String, nullable=False)  # "VIEW_DASHBOARD", "COPY_MESSAGE", "COPY_LINK", "JOIN_ZOOM"
    ip_address = Column(String, nullable=True)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ClassMentorAccount(Base):
    __tablename__ = "class_mentor_accounts"
    id = Column(Integer, primary_key=True, index=True)
    class_category = Column(String, unique=True, index=True, nullable=False)  # "8TH", "9TH", "10TH", "11TH SCI", "11TH COM", "12TH SCI", "12TH COM", "ALL"
    username = Column(String, unique=True, index=True, nullable=False)        # e.g. "mentor8th"
    password_hash = Column(String, nullable=False)
    display_title = Column(String, nullable=False)                            # e.g. "8th Class Mentor"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

