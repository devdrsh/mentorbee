from fastapi import APIRouter, Depends
from app.schemas.zoom import ZoomParseRequest, ZoomParseResponse
from app.services.zoom_parser import parse_zoom_text
from app.routers.admin import get_current_admin

router = APIRouter(prefix="/api/zoom", tags=["zoom"])

@router.post("/parse", response_model=ZoomParseResponse)
def parse_zoom(request: ZoomParseRequest, current_admin = Depends(get_current_admin)):
    return parse_zoom_text(request.text)
