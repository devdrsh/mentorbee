import re
import urllib.parse
from typing import Dict, Optional

def parse_zoom_text(text: str) -> Dict[str, Optional[str]]:
    if not text:
        return {
            "success": False,
            "zoom_link": None,
            "meeting_id": None,
            "passcode": None,
            "errors": ["Input text is empty."]
        }

    # 1. Extract Zoom URL
    # Matches any zoom.us join, webinar, or personal room link
    zoom_link_match = re.search(r'(https://[a-zA-Z0-9.-]*zoom\.us/[^\s*<>"\'`)]+)', text, re.IGNORECASE)
    zoom_link = None
    if zoom_link_match:
        # Strip any trailing punctuation (dots, commas, asterisks, brackets, quotes)
        zoom_link = re.sub(r'[\.,\*\>\)"\'\`]+$', '', zoom_link_match.group(1).strip())

    # Mask URLs from text to avoid false positives (e.g., '?pwd=' in URL matching 'pwd:' regex)
    text_clean = text
    if zoom_link:
        text_clean = text_clean.replace(zoom_link, ' [ZOOM_LINK] ')

    # 2. Extract Meeting ID
    # Try finding explicit "Meeting ID: 812 345 6789" or "ID: 8123456789"
    meeting_id = None
    id_label_match = re.search(
        r'(?:meeting\s*id|webinar\s*id|conf\s*id|\bid)\s*[:=\-]?\s*\*?\s*([\d\s]{9,15})\b',
        text_clean,
        re.IGNORECASE
    )
    if id_label_match:
        meeting_id = re.sub(r'\s+', ' ', id_label_match.group(1)).strip()
    elif zoom_link:
        # Fallback: Extract numeric meeting ID directly from the Zoom URL path (e.g. /j/84930219483 or /w/84930219483)
        url_id_match = re.search(r'zoom\.us/(?:j|w|my)/(\d{9,12})', zoom_link, re.IGNORECASE)
        if url_id_match:
            raw_id = url_id_match.group(1)
            # Format nicely with spaces for readability: e.g. 849 3021 9483 or 879 6543 2101
            if len(raw_id) == 11:
                meeting_id = f"{raw_id[:3]} {raw_id[3:7]} {raw_id[7:]}"
            elif len(raw_id) == 10:
                meeting_id = f"{raw_id[:3]} {raw_id[3:6]} {raw_id[6:]}"
            else:
                meeting_id = raw_id

    # 3. Extract Passcode / Password
    passcode = None
    # Try finding explicit label in clean text: Passcode, Password, Pass code, Pwd, PIN, Security Code
    pass_label_match = re.search(
        r'(?:passcode|password|pass\s*code|\bpwd|\bpin|security\s*code)\s*[:=\-]?\s*\*?\s*([^\s*<>"\'`]+)',
        text_clean,
        re.IGNORECASE
    )
    if pass_label_match:
        passcode = re.sub(r'[\.,\*\>\)"\'\`]+$', '', pass_label_match.group(1)).strip()
    elif zoom_link:
        # Fallback: Extract from the ?pwd= query parameter in the Zoom URL
        pwd_match = re.search(r'[?&]pwd=([a-zA-Z0-9._~-]+)', zoom_link, re.IGNORECASE)
        if pwd_match:
            try:
                passcode = urllib.parse.unquote(pwd_match.group(1).strip())
            except Exception:
                passcode = pwd_match.group(1).strip()


    errors = []
    if not zoom_link:
        errors.append("Zoom link could not be detected.")
    if not meeting_id:
        errors.append("Meeting ID could not be detected.")
    if not passcode:
        errors.append("Passcode could not be found (may not be required).")

    # Success is True as long as we have the Zoom link and Meeting ID
    is_success = bool(zoom_link and meeting_id)

    return {
        "success": is_success,
        "zoom_link": zoom_link,
        "meeting_id": meeting_id,
        "passcode": passcode,
        "errors": errors
    }

