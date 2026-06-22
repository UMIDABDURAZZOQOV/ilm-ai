from typing import Optional

from fastapi import Depends, Header, HTTPException

from services.tokens import verify_access_token


def get_authenticated_user_id(
    authorization: Optional[str] = Header(None),
) -> int:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication required")
    user_id = verify_access_token(authorization[7:])
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user_id


def verify_user_access(
    user_id: int,
    auth_user_id: int = Depends(get_authenticated_user_id),
) -> int:
    if user_id != auth_user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    return user_id


def ensure_own_user(requested_user_id: int, auth_user_id: int) -> None:
    if requested_user_id != auth_user_id:
        raise HTTPException(status_code=403, detail="Access denied")
