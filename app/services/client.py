import httpx
from httpx import Response
from typing import Optional, List
from app.config import settings
from app.models.chat import Chat
from app.models.message import Message
from app.models.user import User
from app.models.token import TokenResponse


class ClientService:
    @staticmethod
    def register_user(username: str, password: str) -> Response:
        data = {"username": username, "password": password}
        response = httpx.post(f"{settings.api_url}/api/users/register", json=data)
        response.raise_for_status()
        return response

    @staticmethod
    def login_user(username: str, password: str) -> Optional[str]:
        data = {"username": username, "password": password}
        response = httpx.post(f"{settings.api_url}/api/users/login", json=data)
        if response.status_code == 200:
            token_response = TokenResponse(**response.json())
            return token_response.access_token
        return None

    @staticmethod
    def get_current_user(token: str) -> User:
        headers = {"Authorization": f"Bearer {token}"}
        response = httpx.get(f"{settings.api_url}/api/users/me", headers=headers)
        response.raise_for_status()
        return User(**response.json())

    @staticmethod
    def get_chats(token: str) -> List[Chat]:
        headers = {"Authorization": f"Bearer {token}"}
        response = httpx.get(f"{settings.api_url}/api/chats/", headers=headers)
        response.raise_for_status()
        return [Chat(**chat) for chat in response.json()]

    @staticmethod
    def get_chat_messages(
        token: str, other_user_id: int, offset: int = 0, limit: int = 50
    ) -> List[Message]:
        headers = {"Authorization": f"Bearer {token}"}
        url = f"{settings.api_url}/api/messages/with/{other_user_id}"
        params = {"offset": offset, "limit": limit}
        response = httpx.get(url, headers=headers, params=params)
        response.raise_for_status()
        return [Message(**msg) for msg in response.json()]

    @staticmethod
    def send_message(token: str, receiver_id: int, content: str) -> Response:
        headers = {"Authorization": f"Bearer {token}"}
        data = {"receiver_id": receiver_id, "content": content}
        response = httpx.post(
            f"{settings.api_url}/api/messages/send", headers=headers, json=data
        )
        response.raise_for_status()
        return response

    @staticmethod
    def search_users(token: str, username: str) -> List[User]:
        headers = {"Authorization": f"Bearer {token}"}
        params = {"username": username}
        response = httpx.get(
            f"{settings.api_url}/api/users/search", headers=headers, params=params
        )
        response.raise_for_status()
        return [User(**user) for user in response.json()]

    @staticmethod
    async def get_updates(
        token: str, last_message_id: int = 0, timeout: int = 30
    ) -> List[Message]:
        headers = {"Authorization": f"Bearer {token}"}
        url = f"{settings.api_url}/api/messages/updates"
        params = {"last_message_id": last_message_id, "timeout": timeout}
        async with httpx.AsyncClient(timeout=timeout + 5) as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return [Message(**msg) for msg in response.json()]

    @staticmethod
    def get_websocket_url(token: str) -> str:
        return f"{settings.ws_url}/api/ws/messages?token={token}"
