from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Batch(Base):
    __tablename__ = "batches"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    class_number = Column(String, nullable=True)  # "8TH", "9TH", "10TH", "11TH", "12TH"
    class_category = Column(String, nullable=True)  # "8TH", "9TH", "10TH", "11TH SCI", "11TH COM", "12TH SCI", "12TH COM"
    syllabus = Column(String, nullable=True)  # "STATE", "CBSE"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    sessions = relationship("ClassSession", back_populates="batch")
