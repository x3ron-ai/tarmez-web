from fastapi import Request
from fastapi.responses import RedirectResponse
from app.services.client import ClientService


def ensure_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        ClientService.get_current_user(token)
    except Exception:
        return None
    return token


def ensure_or_redirect(request: Request):
    token = ensure_token(request)
    if not token:
        return RedirectResponse("/login", status_code=303)
    return token
