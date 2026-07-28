"""
routers/insights.py -- learning insights for the Ilm AI core: a deterministic
roll-up of materials covered, quiz performance/trend, and strong/weak topics.
"""
from fastapi import APIRouter, Depends

from services.auth_deps import verify_user_access
from services.insights import build_insights

router = APIRouter(prefix="/insights", tags=["insights"])


@router.get("/{user_id}")
def get_insights(user_id: int = Depends(verify_user_access)):
    return build_insights(user_id)
