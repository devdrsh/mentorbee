from pydantic import BaseModel
from typing import List, Optional

class ZoomParseRequest(BaseModel):
    text: str

class ZoomParseResponse(BaseModel):
    success: bool
    zoom_link: Optional[str] = None
    meeting_id: Optional[str] = None
    passcode: Optional[str] = None
    errors: List[str] = []
