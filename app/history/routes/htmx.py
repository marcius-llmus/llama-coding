from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi_htmx import htmx

from app.history.dependencies import get_history_page_service, get_history_service
from app.history.exceptions import ChatSessionNotFoundException
from app.history.services import HistoryPageService, HistoryService

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
@htmx("history/partials/session_list")
async def get_history_list(
    request: Request,
    service: HistoryPageService = Depends(get_history_page_service),
):
    page_data = service.get_history_page_data()
    return page_data


@router.delete("/{session_id}", status_code=status.HTTP_200_OK)
async def delete_session(
    request: Request,
    session_id: int,
    service: HistoryService = Depends(get_history_service),
):
    try:
        service.delete_session(session_id=session_id)
        return ""
    except ChatSessionNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))