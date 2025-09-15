from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from app.services.client import ClientService
from app.utils.auth import ensure_or_redirect

router = APIRouter(tags=["ws"])


@router.get("/ws_url")
def get_ws_url(request: Request):
    token = ensure_or_redirect(request)
    if isinstance(token, RedirectResponse):
        return token
    return {"ws_url": ClientService.get_websocket_url(token)}
