from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.api.client import get_chats

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.get("/chats")
def chats(request: Request):
	token = request.cookies.get("access_token")
	if not token:
		return RedirectResponse("/login")
	resp = get_chats(token)
	chats_list = resp.json() if resp.status_code == 200 else []
	return templates.TemplateResponse("chats.html", {"request": request, "chats": chats_list})
