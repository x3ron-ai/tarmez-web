from pydantic import BaseModel
from typing import Optional
from .message import Message

class Chat(BaseModel):
	id: int
	username: str
	last_message: Optional[Message] = None
	updated_at: Optional[str] = None