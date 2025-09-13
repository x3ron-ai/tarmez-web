from fastapi import APIRouter, Request, Form, Response, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.client import ClientService
from app.models.auth import AuthRequest

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(tags=["auth"])

@router.get("/register")
def register_get(request: Request):
	return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
def register_post(request: Request, username: str = Form(...), password: str = Form(...)):
	auth_data = AuthRequest(username=username, password=password)
	resp = ClientService.register_user(auth_data.username, auth_data.password)
	if resp.status_code == 201:
		return RedirectResponse("/login", status_code=303)
	error = resp.json().get("detail", "Ошибка регистрации")
	return templates.TemplateResponse(
		"register.html", {"request": request, "error": error}
	)

@router.get("/login")
def login_get(request: Request):
	return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
	auth_data = AuthRequest(username=username, password=password)
	token = ClientService.login_user(auth_data.username, auth_data.password)
	if token:
		response = RedirectResponse("/chats", status_code=303)
		response.set_cookie(key="access_token", value=token, httponly=True)
		return response
	return templates.TemplateResponse(
		"login.html", {"request": request, "error": "Неверные данные"}
	)

@router.get("/logout")
def logout_get(request: Request):
	response = RedirectResponse("/login", status_code=303)
	response.set_cookie(key="access_token", value="", httponly=True)
	return response