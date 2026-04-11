"""JWT authentication and password hashing for Astro Rattan."""
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRE_HOURS

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=False)

# H1: Separate secret for refresh tokens — derived from JWT_SECRET so only one env var needed
_REFRESH_SECRET = hashlib.sha256(f"{JWT_SECRET}:refresh".encode()).hexdigest()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_token(data: dict, token_version: int = 0) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.now(tz=timezone.utc) + timedelta(hours=JWT_EXPIRE_HOURS)
    to_encode["tv"] = token_version
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)


def create_refresh_token(data: dict, token_version: int = 0) -> str:
    to_encode = data.copy()
    to_encode["type"] = "refresh"
    to_encode["tv"] = token_version
    to_encode["exp"] = datetime.now(tz=timezone.utc) + timedelta(days=7)
    return jwt.encode(to_encode, _REFRESH_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    """Decode a JWT — tries access secret first, then refresh secret."""
    for secret in (JWT_SECRET, _REFRESH_SECRET):
        try:
            return jwt.decode(token, secret, algorithms=[JWT_ALGORITHM])
        except jwt.PyJWTError:
            continue
    return None


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    payload = decode_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    if payload.get("type") == "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh tokens cannot be used for API access")
    # Token revocation check — validate token_version against DB
    token_tv = payload.get("tv", 0)
    user_id = payload.get("sub")
    if user_id:
        from app.database import _get_pool
        try:
            pool = _get_pool()
            conn = pool.getconn()
            try:
                cur = conn.cursor()
                cur.execute("SELECT COALESCE(token_version, 0) FROM users WHERE id = %s", (user_id,))
                row = cur.fetchone()
                if row and row[0] > token_tv:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked — please log in again")
            finally:
                pool.putconn(conn)
        except HTTPException:
            raise
        except Exception:
            pass  # DB down — allow token through, health check will catch it
    return payload


def require_role(*roles: str):
    def role_checker(user: dict = Depends(get_current_user)):
        if user.get("role") not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user
    return role_checker
