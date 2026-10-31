from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime, date

from app.database import get_db
from app.models.session import ClassSession
from app.models.batch import Batch
from app.models.history import SessionChangeHistory
from app.schemas.session import ClassSessionCreate, ClassSessionUpdate, ClassSessionResponse
from app.routers.admin import get_current_admin
from app.websockets import manager
from app.services.message_generator import generate_message

from zoneinfo import ZoneInfo

router = APIRouter(prefix="/api/sessions", tags=["sessions"])
IST = ZoneInfo("Asia/Kolkata")

@router.post("", response_model=ClassSessionResponse)
async def create_session(session: ClassSessionCreate, db: Session = Depends(get_db), current_admin = Depends(get_current_admin)):
    batch = db.query(Batch).filter(Batch.id == session.batch_id).first()
    if not batch:
        raise HTTPException(status_code=400, detail="Invalid batch")
    
    session_data = session.model_dump()
    if not session_data.get("class_category"):
        session_data["class_category"] = batch.class_category or batch.class_number
    
    new_session = ClassSession(**session_data, created_by=current_admin.id, updated_by=current_admin.id)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    await manager.broadcast("update")
    return new_session

def apply_class_filters(query, syllabus: Optional[str], class_category: Optional[str], class_number: Optional[str]):
    query = query.join(ClassSession.batch)
    if syllabus and syllabus.upper() not in ["ALL", "NONE", ""]:
        syl_clean = syllabus.upper().strip()
        if syl_clean in ["EXAM KILLER", "EXAM_KILLER", "EXAMKILLER"]:
            query = query.filter(
                (Batch.syllabus.in_(["EXAM KILLER", "EXAM_KILLER", "EXAMKILLER"])) |
                (Batch.name.ilike("%EXAM%KILLER%"))
            )
        else:
            query = query.filter(Batch.syllabus == syl_clean)
    if class_category:
        cats = [c.strip().upper() for c in class_category.split(",") if c.strip()]
        if cats and "ALL" not in cats:
            # Match either batch.class_category, batch.class_number or session.class_category
            # For 8TH, 9TH, 10TH: could match class_number "8TH" or class_category "8TH"
            query = query.filter(
                (Batch.class_category.in_(cats)) | 
                (Batch.class_number.in_(cats)) |
                (ClassSession.class_category.in_(cats))
            )
    elif class_number:
        query = query.filter(Batch.class_number == class_number.upper())
    return query


@router.get("", response_model=List[ClassSessionResponse])
def get_sessions(
    syllabus: Optional[str] = Query(None),
    class_category: Optional[str] = Query(None),
    class_number: Optional[str] = Query(None),
    session_date: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(ClassSession).options(joinedload(ClassSession.batch))
    if session_date:
        query = query.filter(ClassSession.class_date == session_date)
    if syllabus or class_category or class_number:
        query = apply_class_filters(query, syllabus, class_category, class_number)
    return query.order_by(ClassSession.class_date.desc(), ClassSession.start_time.desc()).all()

@router.get("/today", response_model=List[ClassSessionResponse])
def get_today_sessions(
    syllabus: Optional[str] = Query(None),
    class_category: Optional[str] = Query(None),
    class_number: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    today = datetime.now(IST).date()
    query = db.query(ClassSession).options(joinedload(ClassSession.batch)).filter(ClassSession.class_date == today, ClassSession.is_active == True)
    if syllabus or class_category or class_number:
        query = apply_class_filters(query, syllabus, class_category, class_number)
    return query.order_by(ClassSession.start_time.asc()).all()

@router.get("/upcoming", response_model=List[ClassSessionResponse])
def get_upcoming_sessions(
    syllabus: Optional[str] = Query(None),
    class_category: Optional[str] = Query(None),
    class_number: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    today = datetime.now(IST).date()
    query = db.query(ClassSession).options(joinedload(ClassSession.batch)).filter(ClassSession.class_date > today, ClassSession.is_active == True)
    if syllabus or class_category or class_number:
        query = apply_class_filters(query, syllabus, class_category, class_number)
    return query.order_by(ClassSession.class_date.asc(), ClassSession.start_time.asc()).all()

@router.get("/all", response_model=List[ClassSessionResponse])
def get_all_active_sessions(
    syllabus: Optional[str] = Query(None),
    class_category: Optional[str] = Query(None),
    class_number: Optional[str] = Query(None),
    session_date: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(ClassSession).options(joinedload(ClassSession.batch)).filter(ClassSession.is_active == True)
    if session_date:
        query = query.filter(ClassSession.class_date == session_date)
    if syllabus or class_category or class_number:
        query = apply_class_filters(query, syllabus, class_category, class_number)
    return query.order_by(ClassSession.class_date.desc(), ClassSession.start_time.asc()).all()

@router.get("/{session_id}", response_model=ClassSessionResponse)
def get_session(session_id: int, db: Session = Depends(get_db)):
    session = db.query(ClassSession).options(joinedload(ClassSession.batch)).filter(ClassSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.put("/{session_id}", response_model=ClassSessionResponse)
async def update_session(session_id: int, session: ClassSessionUpdate, db: Session = Depends(get_db), current_admin = Depends(get_current_admin)):
    db_session = db.query(ClassSession).filter(ClassSession.id == session_id).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if db_session.zoom_link != session.zoom_link or db_session.meeting_id != session.meeting_id or db_session.passcode != session.passcode:
        history = SessionChangeHistory(
            session_id=db_session.id,
            changed_by=current_admin.id,
            old_zoom_link=db_session.zoom_link,
            new_zoom_link=session.zoom_link,
            old_meeting_id=db_session.meeting_id,
            new_meeting_id=session.meeting_id,
            old_passcode=db_session.passcode,
            new_passcode=session.passcode
        )
        db.add(history)

    for key, value in session.model_dump(exclude_unset=True).items():
        setattr(db_session, key, value)
    db_session.updated_by = current_admin.id
    db.commit()
    db.refresh(db_session)
    await manager.broadcast("update")
    return db_session

@router.delete("/{session_id}")
async def delete_session(session_id: int, db: Session = Depends(get_db), current_admin = Depends(get_current_admin)):
    db_session = db.query(ClassSession).filter(ClassSession.id == session_id).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db.query(SessionChangeHistory).filter(SessionChangeHistory.session_id == session_id).delete()
    db.delete(db_session)
    db.commit()
    await manager.broadcast("update")
    return {"detail": "Session deleted permanently"}
