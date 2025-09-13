from pydantic import BaseModel
from typing import Optional
from .user import User


class Message(BaseModel):
    id: int
    sender: User
    receiver: User
    content: str
    created_at: Optional[str] = None
