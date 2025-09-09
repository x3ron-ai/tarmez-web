from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.routes import auth, chats, messages, users, ws

app = FastAPI(title="Web Chat Client")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(auth.router)
app.include_router(chats.router)
app.include_router(messages.router)
app.include_router(users.router)
app.include_router(ws.router)

@app.get("/")
def index():
	return RedirectResponse("/chats")