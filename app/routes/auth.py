from fastapi import APIRouter, Request, Form, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.service.client import register_user, login_user

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.get("/register")
def register_get(request: Request):
	return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
def register_post(request: Request, username: str = Form(...), password: str = Form(...)):
	resp = register_user(username, password)
	if resp.status_code == 201:
		return RedirectResponse("/login", status_code=303)
	return templates.TemplateResponse("register.html", {"request": request, "error": resp.text})

@router.get("/login")
def login_get(request: Request):
	return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
	token = login_user(username, password)
	if token:
		response = RedirectResponse("/chats", status_code=303)
		response.set_cookie(key="access_token", value=token, httponly=True)
		return response
	return templates.TemplateResponse("login.html", {"request": request, "error": "Неверные данные"})
