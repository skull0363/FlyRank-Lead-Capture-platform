from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os

pwd_ctx = CryptContext(schemes=["bcrypt"])

JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    raise RuntimeError(
        "JWT_SECRET is not set. Add JWT_SECRET=<a-long-random-string> to your .env file."
    )


def hash_password(pw: str) -> str:
    return pwd_ctx.hash(pw)


def verify_password(pw: str, hashed: str) -> bool:
    return pwd_ctx.verify(pw, hashed)


def create_token(tenant_id: str) -> str:
    payload = {"sub": tenant_id, "exp": datetime.utcnow() + timedelta(days=7)}
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")


def decode_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])