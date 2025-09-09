from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi_csrf_protect import CsrfProtect

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
async def chats(request: Request, csrf_protect: CsrfProtect = Depends()):
	token = request.cookies.get("access_token")
	if not token:
		return RedirectResponse("/login")
	csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
	response = templates.TemplateResponse("chats.html", {"request": request, "csrf_token": csrf_token})
	csrf_protect.set_csrf_cookie(signed_token, response)
	return response