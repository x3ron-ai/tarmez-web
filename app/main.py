from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from app.routes import auth, chats, messages, users, ws
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError

from pydantic import BaseModel

app = FastAPI(title="Web Chat Client")

app.include_router(auth.router)
app.include_router(chats.router)
app.include_router(messages.router)
app.include_router(users.router)
app.include_router(ws.router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

class CsrfSettings(BaseModel):
	secret_key: str = "your-secret-key"
	cookie_samesite: str = "lax"

@CsrfProtect.load_config
def get_csrf_config():
	return CsrfSettings()

@app.get("/ping")
def index():
	return {"response":"pong"}

@app.get("/")
def index():
	return RedirectResponse("/chats")

@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
	return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
