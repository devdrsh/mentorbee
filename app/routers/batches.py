from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import re

from app.database import get_db
from app.models.batch import Batch
from app.schemas.batch import BatchCreate, BatchUpdate, BatchResponse
from app.routers.admin import get_current_admin

router = APIRouter(prefix="/api/batches", tags=["batches"])

def infer_syllabus(name: str) -> str:
    upper = name.upper()
    if "EXAM KILLER" in upper or "EXAMKILLER" in upper or "EXAM_KILLER" in upper:
        return "EXAM KILLER"
    elif "STATE" in upper:
        return "STATE"
    elif "CBSE" in upper:
        return "CBSE"
    return "OTHER"

def infer_class_number(name: str) -> str:
    m = re.match(r"^(\d+(?:TH|ST|ND|RD)?)\b", name, re.IGNORECASE)
    if m:
        return m.group(1).upper()
    m2 = re.search(r"\b(8TH|9TH|10TH|11TH|12TH|8|9|10|11|12)\b", name, re.IGNORECASE)
    if m2:
        val = m2.group(1).upper()
        return val if "TH" in val else f"{val}TH"
    return ""

def infer_class_category(name: str) -> str:
    name_upper = name.upper()
    if "8TH" in name_upper or "CLASS 8" in name_upper:
        return "8TH"
    if "9TH" in name_upper or "CLASS 9" in name_upper:
        return "9TH"
    if "10TH" in name_upper or "CLASS 10" in name_upper or "SSLC" in name_upper:
        return "10TH"
    if "11TH" in name_upper or "CLASS 11" in name_upper or "PLUS ONE" in name_upper:
        if "COM" in name_upper or "COMMERCE" in name_upper:
            return "11TH COM"
        return "11TH SCI"
    if "12TH" in name_upper or "CLASS 12" in name_upper or "PLUS TWO" in name_upper:
        if "COM" in name_upper or "COMMERCE" in name_upper:
            return "12TH COM"
        return "12TH SCI"
    if "EXAM KILLER" in name_upper or "EXAMKILLER" in name_upper:
        return "EXAM KILLER"
    return "OTHER"


@router.post("", response_model=BatchResponse)
def create_batch(batch: BatchCreate, db: Session = Depends(get_db), current_admin = Depends(get_current_admin)):
    clean_name = " ".join(batch.name.strip().split()).upper()
    db_batch = db.query(Batch).filter(Batch.name == clean_name).first()
    if db_batch:
        raise HTTPException(status_code=400, detail="Batch with this name already exists")
    
    data = batch.model_dump()
    data['name'] = clean_name
    if not data.get('syllabus'):
        data['syllabus'] = infer_syllabus(clean_name)
    if not data.get('class_number'):
        data['class_number'] = infer_class_number(clean_name)
    if not data.get('class_category'):
        data['class_category'] = infer_class_category(clean_name)

    new_batch = Batch(**data)
    db.add(new_batch)
    db.commit()
    db.refresh(new_batch)
    return new_batch

@router.get("", response_model=List[BatchResponse])
def get_batches(
    syllabus: Optional[str] = Query(None),
    class_category: Optional[str] = Query(None),
    class_number: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Batch).filter(Batch.is_active == True)
    if syllabus and syllabus.upper() in ["STATE", "CBSE"]:
        query = query.filter(Batch.syllabus == syllabus.upper())
    if class_category:
        cats = [c.strip().upper() for c in class_category.split(",") if c.strip()]
        if cats and "ALL" not in cats:
            query = query.filter(Batch.class_category.in_(cats))
    elif class_number:
        query = query.filter(Batch.class_number == class_number.upper())
    return query.order_by(Batch.syllabus.asc(), Batch.name.asc()).all()

@router.put("/{batch_id}", response_model=BatchResponse)
def update_batch(batch_id: int, batch: BatchUpdate, db: Session = Depends(get_db), current_admin = Depends(get_current_admin)):
    db_batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if not db_batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    data = batch.model_dump(exclude_unset=True)
    if 'name' in data:
        data['name'] = " ".join(data['name'].strip().split()).upper()
        if not data.get('syllabus') and not db_batch.syllabus:
            data['syllabus'] = infer_syllabus(data['name'])
        if not data.get('class_number') and not db_batch.class_number:
            data['class_number'] = infer_class_number(data['name'])

    for key, value in data.items():
        setattr(db_batch, key, value)
    db.commit()
    db.refresh(db_batch)
    return db_batch
