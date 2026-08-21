import re
from typing import Dict, Optional

def parse_zoom_text(text: str) -> Dict[str, Optional[str]]:
    # 1. Extract Zoom URL
    # Looks for https://zoom.us/j/ followed by non-whitespace
    zoom_link_match = re.search(r'(https://[a-zA-Z0-9.-]*zoom\.us/[^\s*]+)', text)
    zoom_link = zoom_link_match.group(1) if zoom_link_match else None

    # 2. Extract Meeting ID
    # Looks for "Meeting ID:" or similar, then captures numbers (can have spaces)
    # Ignoring markdown asterisks
    meeting_id_match = re.search(r'meeting\s*id\s*:?\s*\*?\s*([\d\s]+)\*?', text, re.IGNORECASE)
    meeting_id = meeting_id_match.group(1).strip() if meeting_id_match else None

    # 3. Extract Passcode
    passcode_match = re.search(r'passcode\s*:?\s*\*?\s*([^\s*]+)\*?', text, re.IGNORECASE)
    passcode = passcode_match.group(1).strip() if passcode_match else None

    errors = []
    if not zoom_link:
        errors.append("Zoom link could not be found.")
    if not meeting_id:
        errors.append("Meeting ID could not be found.")
    if not passcode:
        errors.append("Passcode could not be found.")

    return {
        "success": len(errors) == 0,
        "zoom_link": zoom_link,
        "meeting_id": meeting_id,
        "passcode": passcode,
        "errors": errors
    }
