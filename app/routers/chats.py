from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi_csrf_protect import CsrfProtect
from app.services.client import ClientService
from app.models.chat import Chat
from typing import List
from app.utils.auth import ensure_or_redirect

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(tags=["chats"])


@router.get("/chats/list", response_model=List[Chat])
def chat_list(request: Request):
    token = ensure_or_redirect(request)
    if isinstance(token, RedirectResponse):
        return token
    return ClientService.get_chats(token)


@router.get("/chats")
async def chats(request: Request, csrf_protect: CsrfProtect = Depends()):
    token = ensure_or_redirect(request)
    if isinstance(token, RedirectResponse):
        return token

    csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
    response = templates.TemplateResponse(
        "chats.html", {"request": request, "csrf_token": csrf_token}
    )
    csrf_protect.set_csrf_cookie(signed_token, response)
    return response
