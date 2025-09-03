from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from app.api.client import search_users

router = APIRouter()

@router.get("/search")
def chats(request: Request, username: str):
	token = request.cookies.get("access_token")	
	if not token:
		return RedirectResponse("/login")
	resp = search_users(token, username)
	users = resp.json() if resp.status_code == 200 else []
	return users
		