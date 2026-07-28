"""
routers/insights.py -- learning insights for the Ilm AI core: a deterministic
roll-up of materials covered, quiz performance/trend, and strong/weak topics.
"""
from fastapi import APIRouter, Depends

from services.auth_deps import verify_user_access
from services.insights import build_insights

router = APIRouter(prefix="/insights", tags=["insights"])


@router.get("/gamify/{user_id}")
def gamify_stats(user_id: int = Depends(verify_user_access)):
    """XP and streak for the Ilm AI home card — the same streak the whole app shares."""
    from services.gamify import get_stats
    return get_stats(user_id)


@router.get("/{user_id}")
def get_insights(user_id: int = Depends(verify_user_access)):
    return build_insights(user_id)
