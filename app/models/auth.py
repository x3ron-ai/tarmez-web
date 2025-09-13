from pydantic import BaseModel, Field


class AuthRequest(BaseModel):
    username: str
    password: str
