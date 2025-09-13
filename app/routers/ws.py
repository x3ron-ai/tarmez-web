from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from app.services.client import ClientService

router = APIRouter(tags=["ws"])


@router.get("/ws_url")
def get_ws_url(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse("/login")

    return {"ws_url": ClientService.get_websocket_url(token)}
