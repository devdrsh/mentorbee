import sys
import os
import re

sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)))

from app.database import SessionLocal
from app.models.batch import Batch

STATE_BATCH_NAMES = [
    "8TH STATE ONLINE BATCH",
    "8TH STATE OFFLINE BATCH",
    "8TH STATE OFFLINE HO BATCH",
    "8TH STATE OFFLINE EDA BATCH",
    "8TH STATE OFFLINE PON BATCH",
    "8TH STATE OFFLINE THE BATCH",
    "8TH STATE ONLINE MNG BATCH",
    "9TH STATE ONLINE MNG BATCH",
    "9TH STATE ONLINE EVNG BATCH",
    "9TH STATE OFFLINE BATCH",
    "9TH STATE OFFLINE HO BATCH",
    "9TH STATE OFFLINE EDA BATCH",
    "9TH STATE OFFLINE PON BATCH",
    "10TH STATE ONLINE MNG BATCH",
    "10TH STATE ONLINE EVNG BATCH",
    "10TH STATE OFFLINE BATCH",
    "10TH STATE OFFLINE HO BATCH",
    "10TH STATE OFFLINE EDA BATCH",
    "10TH STATE OFFLINE PON BATCH",
    "11TH STATE SCI ONLINE MNG BATCH",
    "11TH STATE SCI ONLINE EVNG BATCH",
    "11TH STATE SCI OFFLINE BATCH",
    "11TH STATE SCI OFFLINE HO BATCH",
    "11TH STATE SCI OFFLINE EDA BATCH",
    "11TH STATE SCI OFFLINE PON BATCH",
    "9TH STATE OFFLINE THE BATCH",
    "10TH STATE OFFLINE THE BATCH",
    "11TH STATE COM OFFLINE THE BATCH",
    "11TH STATE COM ONLINE MNG BATCH",
    "11TH STATE COM ONLINE EVNG BATCH",
    "11TH STATE COM OFFLINE BATCH",
    "11TH STATE COM OFFLINE HO BATCH",
    "11TH STATE COM OFFLINE EDA BATCH",
    "11TH STATE COM OFFLINE PON BATCH",
    "12TH STATE COM OFFLINE THE BATCH",
    "12TH STATE COM ONLINE MNG BATCH",
    "12TH STATE COM ONLINE EVNG BATCH",
    "12TH STATE COM OFFLINE BATCH",
    "12TH STATE COM OFFLINE HO BATCH",
    "12TH STATE COM OFFLINE EDA BATCH",
    "12TH STATE COM OFFLINE PON BATCH",
    "12TH STATE SCI OFFLINE THE BATCH",
    "12TH STATE SCI ONLINE MNG BATCH",
    "12TH STATE SCI ONLINE EVNG BATCH",
    "12TH STATE SCI OFFLINE BATCH",
    "12TH STATE SCI OFFLINE HO BATCH",
    "12TH STATE SCI OFFLINE EDA BATCH",
    "8TH STATE EXAM ID",
    "9TH STATE EXAM ID",
    "10TH STATE EXAM ID",
]

CBSE_BATCH_NAMES = [
    "8TH CBSE EVNG BATCH",
    "8TH CBSE MNG BATCH",
    "8TH CBSE MNG KL BATCH",
    "8TH CBSE MNG AB BATCH",
    "8TH CBSE EVNG KL BATCH",
    "8TH CBSE EVNG AB BATCH",
    "8TH CBSE EXAM ID",
    "9TH CBSE MNG KL BATCH",
    "9TH CBSE MNG AB BATCH",
    "9TH CBSE EVNG KL BATCH",
    "9TH CBSE EVNG AB BATCH",
    "9TH CBSE EXAM ID",
    "10TH CBSE MNG KL BATCH",
    "10TH CBSE MNG AB BATCH",
    "10TH CBSE EVNG KL BATCH",
    "10TH CBSE EVNG AB BATCH",
    "10TH CBSE EXAM ID",
    "11TH CBSE SCI MNG KL BATCH",
    "11TH CBSE SCI MNG AB BATCH",
    "11TH CBSE SCI EVNG KL BATCH",
    "11TH CBSE SCI EVNG AB BATCH",
    "11TH CBSE SCI CS BATCH",
    "11TH CBSE SCI BIO BATCH",
    "11TH CBSE SCIENCE EXAM ID",
    "11TH CBSE COM MNG KL BATCH",
    "11TH CBSE COM MNG AB BATCH",
    "11TH CBSE COM EVNG KL BATCH",
    "11TH CBSE COM EVNG AB BATCH",
    "11TH CBSE COM IP BATCH",
    "11TH CBSE COM MATHS BATCH",
    "11TH CBSE COMMERCE EXAM ID",
    "12TH CBSE SCI MNG KL BATCH",
    "12TH CBSE SCI MNG AB BATCH",
    "12TH CBSE SCI EVNG KL BATCH",
    "12TH CBSE SCI EVNG AB BATCH",
    "12TH CBSE SCI CS BATCH",
    "12TH CBSE SCI BIO BATCH",
    "12TH CBSE SCIENCE EXAM ID",
    "12TH CBSE COM MNG KL BATCH",
    "12TH CBSE COM MNG AB BATCH",
    "12TH CBSE COM EVNG KL BATCH",
    "12TH CBSE COM EVNG AB BATCH",
    "12TH CBSE COM IP BATCH",
    "12TH CBSE COM MATHS BATCH",
    "12TH CBSE COMMERCE EXAM ID",
]

def extract_class_number(name: str) -> str:
    m = re.match(r"^(\d+(?:TH|ST|ND|RD)?)\b", name, re.IGNORECASE)
    if m:
        return m.group(1).upper()
    return ""

def extract_class_category(name: str) -> str:
    name_upper = name.upper()
    if name_upper.startswith("8TH") or name_upper.startswith("8"):
        return "8TH"
    if name_upper.startswith("9TH") or name_upper.startswith("9"):
        return "9TH"
    if name_upper.startswith("10TH") or name_upper.startswith("10"):
        return "10TH"
    if name_upper.startswith("11TH") or name_upper.startswith("11"):
        if "COM" in name_upper or "COMMERCE" in name_upper:
            return "11TH COM"
        return "11TH SCI"
    if name_upper.startswith("12TH") or name_upper.startswith("12"):
        if "COM" in name_upper or "COMMERCE" in name_upper:
            return "12TH COM"
        return "12TH SCI"
    return "OTHER"

def populate():
    db = SessionLocal()
    created_count = 0
    updated_count = 0
    skipped_count = 0

    # Clean normalize names
    seen_names = set()

    # Process State batches
    for raw_name in STATE_BATCH_NAMES:
        name = " ".join(raw_name.strip().split()).upper()
        if name in seen_names:
            continue
        seen_names.add(name)
        class_num = extract_class_number(name)
        class_cat = extract_class_category(name)
        
        batch = db.query(Batch).filter(Batch.name == name).first()
        if not batch:
            batch = Batch(
                name=name,
                class_number=class_num,
                class_category=class_cat,
                syllabus="STATE",
                is_active=True
            )
            db.add(batch)
            created_count += 1
        else:
            batch.syllabus = "STATE"
            batch.class_number = class_num
            batch.class_category = class_cat
            batch.is_active = True
            updated_count += 1

    # Process CBSE batches
    for raw_name in CBSE_BATCH_NAMES:
        name = " ".join(raw_name.strip().split()).upper()
        if name in seen_names:
            continue
        seen_names.add(name)
        class_num = extract_class_number(name)
        class_cat = extract_class_category(name)
        
        batch = db.query(Batch).filter(Batch.name == name).first()
        if not batch:
            batch = Batch(
                name=name,
                class_number=class_num,
                class_category=class_cat,
                syllabus="CBSE",
                is_active=True
            )
            db.add(batch)
            created_count += 1
        else:
            batch.syllabus = "CBSE"
            batch.class_number = class_num
            batch.class_category = class_cat
            batch.is_active = True
            updated_count += 1

    # Update any existing legacy batches syllabus & class_category based on name
    all_batches = db.query(Batch).all()
    for b in all_batches:
        if not b.syllabus:
            if "STATE" in b.name.upper():
                b.syllabus = "STATE"
            elif "CBSE" in b.name.upper():
                b.syllabus = "CBSE"
            else:
                b.syllabus = "OTHER"
        if not b.class_number:
            b.class_number = extract_class_number(b.name)
        b.class_category = extract_class_category(b.name)
        updated_count += 1

    db.commit()
    
    total_state = db.query(Batch).filter(Batch.syllabus == "STATE").count()
    total_cbse = db.query(Batch).filter(Batch.syllabus == "CBSE").count()
    total_all = db.query(Batch).count()
    
    print(f"Populate complete:")
    print(f"- Newly Created: {created_count}")
    print(f"- Updated: {updated_count}")
    print(f"- Total STATE Batches: {total_state}")
    print(f"- Total CBSE Batches: {total_cbse}")
    print(f"- Total All Batches: {total_all}")
    
    db.close()

if __name__ == "__main__":
    populate()
