from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os

pwd_ctx = CryptContext(schemes=["bcrypt"])
JWT_SECRET = os.getenv("JWT_SECRET")

def hash_password(pw): return pwd_ctx.hash(pw)
def verify_password(pw, hashed): return pwd_ctx.verify(pw, hashed)

def create_token(tenant_id: str):
    payload = {"sub": tenant_id, "exp": datetime.utcnow() + timedelta(days=7)}
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def decode_token(token: str):
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])