from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi_csrf_protect import CsrfProtect
from app.services.client import ClientService
from app.models.message import Message
from typing import List
from app.utils.auth import ensure_or_redirect

router = APIRouter(tags=["messages"])


@router.get("/chat/{user_id}", response_model=List[Message])
def get_chat(user_id: int, request: Request, offset: int = 0, limit: int = 50):
    token = ensure_or_redirect(request)
    if isinstance(token, RedirectResponse):
        return token
    return ClientService.get_chat_messages(token, user_id, offset=offset, limit=limit)


@router.post("/chat/{user_id}/send")
async def send_msg(
    request: Request,
    user_id: int,
    content: str = Form(...),
    csrf_token: CsrfProtect = Depends(),
):
    token = ensure_or_redirect(request)
    if isinstance(token, RedirectResponse):
        return token
    await csrf_token.validate_csrf(request)
    ClientService.send_message(token, user_id, content)
    return RedirectResponse(f"/chat/{user_id}", status_code=303)


@router.get("/updates", response_model=List[Message])
async def updates(request: Request, last_message_id: int = 0, timeout: int = 30):
    token = ensure_or_redirect(request)
    if isinstance(token, RedirectResponse):
        return token
    messages = await ClientService.get_updates(
        token, last_message_id=last_message_id, timeout=timeout
    )
    return messages
