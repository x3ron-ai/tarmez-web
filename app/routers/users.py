from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from app.services.client import ClientService
from app.models.user import User
from typing import List
from app.utils.auth import ensure_or_redirect

router = APIRouter(tags=["users"])


@router.get("/search", response_model=List[User])
def search(request: Request, username: str):
    token = ensure_or_redirect(request)
    if isinstance(token, RedirectResponse):
        return token
    return ClientService.search_users(token, username)
