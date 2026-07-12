from fastapi import APIRouter, Depends
from pydantic import BaseModel

from services.auth_deps import ensure_own_user, get_authenticated_user_id
from services.users import set_push_token

router = APIRouter(prefix="/notifications", tags=["notifications"])


class RegisterTokenRequest(BaseModel):
    user_id: int
    token: str


@router.post("/register-token")
def register_token(
    data: RegisterTokenRequest,
    auth_user_id: int = Depends(get_authenticated_user_id),
):
    ensure_own_user(data.user_id, auth_user_id)
    ok = set_push_token(data.user_id, data.token)
    if not ok:
        return {"error": "User not found"}
    return {"message": "Push token registered"}
