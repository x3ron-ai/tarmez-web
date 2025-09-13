from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from app.services.client import ClientService
from app.models.user import User
from typing import List

router = APIRouter(tags=["users"])


@router.get("/search", response_model=List[User])
def search(request: Request, username: str):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse("/login")
    return ClientService.search_users(token, username)
