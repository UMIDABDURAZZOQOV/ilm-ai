from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from services.auth_deps import verify_user_access, ensure_own_user, get_authenticated_user_id
from services.review import list_due, complete_review

router = APIRouter(prefix="/review", tags=["review"])


class CompleteReviewRequest(BaseModel):
    user_id: int
    score: int
    total: int


@router.get("/due/{user_id}")
def get_due_reviews(user_id: int = Depends(verify_user_access)):
    return {"due": list_due(user_id)}


@router.post("/{item_id}/complete")
def complete_review_item(
    item_id: int,
    data: CompleteReviewRequest,
    auth_user_id: int = Depends(get_authenticated_user_id),
):
    ensure_own_user(data.user_id, auth_user_id)
    item = complete_review(item_id, data.user_id, data.score, data.total)
    if not item:
        raise HTTPException(status_code=404, detail="Review item not found")
    return item
