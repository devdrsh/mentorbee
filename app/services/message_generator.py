import re
from datetime import date, time
from typing import Optional
from app.models.batch import Batch
from app.models.session import ClassSession

def format_meeting_id(meeting_id: str) -> str:
    clean_id = (meeting_id or "").strip()
    if " " in clean_id:
        return clean_id
    digits = re.sub(r"\D", "", clean_id)
    if len(digits) == 11:
        return f"{digits[:3]} {digits[3:7]} {digits[7:]}"
    elif len(digits) == 10:
        return f"{digits[:3]} {digits[3:6]} {digits[6:]}"
    return clean_id

def is_exam_killer_batch(batch: Optional[Batch], session: Optional[ClassSession] = None) -> bool:
    if session and session.class_category:
        cat = session.class_category.upper().strip()
        if "EXAM KILLER" in cat or "EXAMKILLER" in cat:
            return True

    if batch:
        syllabus = (batch.syllabus or "").upper().strip()
        if syllabus in ["EXAM KILLER", "EXAM_KILLER", "EXAMKILLER"]:
            return True
        category = (batch.class_category or "").upper().strip()
        if "EXAM KILLER" in category or "EXAMKILLER" in category:
            return True
        name = (batch.name or "").upper().strip()
        if any(k in name for k in ["EXAM KILLER", "EXAMKILLER", "REV-", "REVISE", "REVISION"]):
            return True

    return False

def generate_message(batch: Optional[Batch], session: ClassSession) -> str:
    # Example format required:
    # *MENTORBEE EDUVERSE*
    # *EXAM KILLER 4.0 - REVISE*
    # *10TH CBSE KL REV-2 BATCH (2)* 
    # -----------------------------------
    # *TOPIC : CHEMISTRY*
    # *DATE : OCTOBER 26, 2026*
    # *TIME : 06:00 PM IST*
    #
    #
    # *Join Zoom Meeting*
    # https://us06web.zoom.us/j/89982457863?pwd=cDv1PpMA7zYEjbQ3kVgZGqbbwakqi3.1
    #
    # *Meeting ID: 899 8245 7863*
    # *Passcode: mentorbee*

    # Formatting date
    date_formatted = session.class_date.strftime("%B %d, %Y").upper()

    # Formatting time
    time_formatted = session.start_time.strftime("%I:%M %p")

    # Formatting meeting ID
    meeting_id_formatted = format_meeting_id(session.meeting_id)

    batch_name = (batch.name if batch else (session.class_category or "BATCH")).upper().strip()
    topic = session.topic.upper().strip()
    zoom_link = session.zoom_link.strip()
    passcode = session.passcode.strip()

    header_lines = ["*MENTORBEE EDUVERSE*"]
    if is_exam_killer_batch(batch, session):
        header_lines.append("*EXAM KILLER 4.0 - REVISE*")
    header_lines.append(f"*{batch_name}*")
    header_block = "\n".join(header_lines)

    return f"""{header_block}
-----------------------------------
*TOPIC : {topic}*
*DATE : {date_formatted}*
*TIME : {time_formatted} IST*


*Join Zoom Meeting*
{zoom_link}

*Meeting ID: {meeting_id_formatted}*
*Passcode: {passcode}*"""
