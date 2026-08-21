from datetime import date, time
from app.models.batch import Batch
from app.models.session import ClassSession

def generate_message(batch: Batch, session: ClassSession) -> str:
    # Example format required:
    # *MENTORBEE EDUVERSE*
    # *12TH CBSE SCIENCE KL - BATCH*
    # ---------------------------------------
    # *TOPIC : CHEMISTRY*
    # *DATE : AUGUST 16, 2026*
    # *TIME : 07:00 PM IST*
    #
    # *Join Zoom Meeting*
    # https://zoom.us/j/92399684884?pwd=1Mpin1EX7SFEbIsZp8QApqkeFaRA7G.1
    #
    # *Meeting ID: 923 9968 4884*
    # *Passcode: mentorbee*

    # Formatting date
    date_formatted = session.class_date.strftime("%B %d, %Y").upper()

    # Formatting time
    time_formatted = session.start_time.strftime("%I:%M %p")

    return f"""*MENTORBEE EDUVERSE*
*{batch.name.upper()}*
---------------------------------------
*TOPIC : {session.topic.upper()}*
*DATE : {date_formatted}*
*TIME : {time_formatted} IST*


*Join Zoom Meeting*
{session.zoom_link}

*Meeting ID: {session.meeting_id}*
*Passcode: {session.passcode}*"""
