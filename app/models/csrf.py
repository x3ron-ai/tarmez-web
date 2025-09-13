from pydantic import BaseModel


class CsrfSettings(BaseModel):
    secret_key: str
    cookie_samesite: str = "lax"
