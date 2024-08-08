import secrets
from fastapi import Request
def get_session_id_from_cookie(request: Request) -> str:
    return request.cookies.get("session_id")

def generate_session_id() -> str:
    return secrets.token_hex(16)