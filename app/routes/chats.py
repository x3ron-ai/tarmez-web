from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.service.client import get_chats

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.get("/chats/list")
def chat_list(request: Request):
	token = request.cookies.get("access_token")
	if not token:
		raise HTTPException(status_code=401, detail="Unauthorized")
	
	resp = get_chats(token)
	chats_list = resp.json() if resp.status_code == 200 else []
	return chats_list

@router.get("/chats")
def chats(request: Request):
	token = request.cookies.get("access_token")
	if not token:
		return RedirectResponse("/login")
	return templates.TemplateResponse("chats.html", {"request": request})