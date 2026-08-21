from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Time, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class ClassSession(Base):
    __tablename__ = "class_sessions"
    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batches.id"), nullable=False)
    class_category = Column(String, nullable=True)  # "8TH", "9TH", "10TH", "11TH SCI", "11TH COM", "12TH SCI", "12TH COM"
    topic = Column(String, nullable=False)
    class_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    zoom_link = Column(Text, nullable=False)
    meeting_id = Column(String, nullable=False)
    passcode = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("admin_users.id"), nullable=True)
    updated_by = Column(Integer, ForeignKey("admin_users.id"), nullable=True)

    batch = relationship("Batch", back_populates="sessions")

    @property
    def formatted_message(self) -> str:
        from app.services.message_generator import generate_message
        if self.batch:
            return generate_message(self.batch, self)
        return ""
