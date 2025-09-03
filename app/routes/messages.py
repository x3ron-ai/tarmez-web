from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.api.client import get_chat_messages, send_message, get_updates
from fastapi.responses import JSONResponse

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.get("/chat/{user_id}")
def chat(request: Request, user_id: int):
	token = request.cookies.get("access_token")
	if not token:
		return RedirectResponse("/login")
	resp = get_chat_messages(token, user_id)
	print(resp.json())
	messages = resp.json() if resp.status_code == 200 else []
	return templates.TemplateResponse("chat.html", {"request": request, "messages": messages, "user_id": user_id})

@router.post("/chat/{user_id}/send")
def send_msg(request: Request, user_id: int, content: str = Form(...)):
	token = request.cookies.get("access_token")
	if not token:
		return RedirectResponse("/login")
	send_message(token, receiver_id=user_id, content=content)
	return RedirectResponse(f"/chat/{user_id}", status_code=303)

@router.get("/updates")
async def updates(request: Request, last_message_id: int = 0, timeout: int = 30):
	token = request.cookies.get("access_token")
	resp = await get_updates(token, last_message_id=last_message_id, timeout=timeout)
	return JSONResponse(resp.json())