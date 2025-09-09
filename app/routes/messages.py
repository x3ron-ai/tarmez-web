from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi_csrf_protect import CsrfProtect

from app.service.client import get_chat_messages, send_message, get_updates

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.get("/chat/{user_id}")
def get_chat(user_id: int, request: Request, offset: int = 0, limit: int = 50):
	token = request.cookies.get("access_token")
	if not token:
		raise HTTPException(status_code=401, detail="Unauthorized")

	resp = get_chat_messages(token, user_id, offset=offset, limit=limit)

	if resp.status_code != 200:
		raise HTTPException(status_code=resp.status_code, detail="Error fetching messages")

	messages = resp.json()
	return {"user_id": user_id, "messages": messages}

@router.post("/chat/{user_id}/send")
async def send_msg(request: Request, user_id: int, content: str = Form(...), csrf_token: CsrfProtect = Depends()):
	token = request.cookies.get("access_token")
	if not token:
		return RedirectResponse("/login")
	await csrf_token.validate_csrf(request)
	send_message(token, user_id, content)
	return RedirectResponse(f"/chat/{user_id}", status_code=303)

@router.get("/updates")
async def updates(request: Request, last_message_id: int = 0, timeout: int = 30):
	token = request.cookies.get("access_token")
	resp = await get_updates(token, last_message_id=last_message_id, timeout=timeout)
	return JSONResponse(resp.json())