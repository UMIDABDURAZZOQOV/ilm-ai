"""Versioned mobile entry point; existing /skills contracts remain available."""

from fastapi import APIRouter, Depends

from routers import skills, tutor
from services.mobile_publication import mobile_publication, published_subjects
from services.auth_deps import verify_user_access
from services.db import get_db

router = APIRouter(prefix="/mobile", dependencies=[Depends(mobile_publication)])


@router.get("/skills/config")
def mobile_config():
    return {"mobile_curriculum_version": 1, "subjects": sorted(published_subjects()),
            "content_language": "uz", "grades": list(range(5, 12))}


@router.get("/skills/{user_id}/preferences")
def mobile_preferences(user_id: int = Depends(verify_user_access), db=Depends(get_db)):
    return visible_preferences(skills.get_study_preferences(user_id, db))


def visible_preferences(payload):
    values = payload.get("preferences")
    if values:
        # Hide old selections in the mobile response without overwriting them.
        values = dict(values)
        if values.get("subject") not in published_subjects():
            values.pop("subject", None)
        if values.get("grade") not in [str(g) for g in range(5, 12)]:
            values.pop("grade", None)
        payload = {"preferences": values}
    return payload


@router.post("/skills/{user_id}/preferences")
def save_mobile_preferences(data: skills.StudyPreferencesRequest,
                            user_id: int = Depends(verify_user_access), db=Depends(get_db)):
    return visible_preferences(skills.save_study_preferences(data, user_id, db))


router.include_router(skills.router)
router.include_router(tutor.router)
