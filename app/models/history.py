from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class SessionChangeHistory(Base):
    __tablename__ = "session_change_history"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("class_sessions.id"), nullable=False)
    changed_by = Column(Integer, ForeignKey("admin_users.id"), nullable=True)
    changed_at = Column(DateTime(timezone=True), server_default=func.now())
    old_zoom_link = Column(Text, nullable=True)
    new_zoom_link = Column(Text, nullable=True)
    old_meeting_id = Column(String, nullable=True)
    new_meeting_id = Column(String, nullable=True)
    old_passcode = Column(String, nullable=True)
    new_passcode = Column(String, nullable=True)
    reason = Column(Text, nullable=True)
