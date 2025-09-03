import httpx
from typing import Optional
from app.config import settings

def register_user(username: str, password: str):
	data = {"username": username, "password": password}
	response = httpx.post(f"{settings.api_url}/api/users/register", json=data)
	return response

def login_user(username: str, password: str):
	data = {"username": username, "password": password}
	response = httpx.post(f"{settings.api_url}/api/users/login", json=data)
	if response.status_code == 200:
		return response.json()["access_token"]
	return None

def get_current_user(token: str):
	headers = {"Authorization": f"Bearer {token}"}
	response = httpx.get(f"{settings.api_url}/api/users/me", headers=headers)
	return response

def get_chats(token: str):
	headers = {"Authorization": f"Bearer {token}"}
	response = httpx.get(f"{settings.api_url}/api/chats/", headers=headers)
	return response

def get_chat_messages(token: str, other_user_id: int, offset: int = 0, limit: int = 50):
	headers = {"Authorization": f"Bearer {token}"}
	url = f"{settings.api_url}/api/messages/with/{other_user_id}"
	params = {"offset": offset, "limit": limit}
	response = httpx.get(url, headers=headers, params=params)
	return response

def send_message(token: str, receiver_id: int, content: str):
	headers = {"Authorization": f"Bearer {token}"}
	data = {"receiver_id": receiver_id, "content": content}
	response = httpx.post(f"{settings.api_url}/api/messages/send", headers=headers, json=data)
	return response

def search_users(token: str, username : str):
	headers = {"Authorization": f"Bearer {token}"}
	params = {"username": username}
	response = httpx.get(f"{settings.api_url}/api/users/search", headers=headers, params=params)
	return response

async def get_updates(token: str, last_message_id: int = 0, timeout: int = 30):
	headers = {"Authorization": f"Bearer {token}"}
	url = f"{settings.api_url}/api/messages/updates"
	params = {"last_message_id": last_message_id, "timeout": timeout}
	async with httpx.AsyncClient(timeout=timeout+5) as client:
		response = await client.get(url, headers=headers, params=params)
		return response
