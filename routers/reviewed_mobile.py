"""Production contracts reuse the shared engines, never loopback test identity."""

from fastapi import APIRouter, Depends
from routers.beta_mobile import create_router
from services.reviewed_mobile_release import publication_db

router = APIRouter()


@router.get("/mobile/skills/config", dependencies=[Depends(publication_db)])
def config():
    from services.beta_curriculum import SUBJECTS

    return {
        "mobile_curriculum_version": 2,
        "subjects": list(SUBJECTS),
        "content_language": "uz",
        "grades": list(range(5, 12)),
    }


router.include_router(create_router("/mobile", publication_db))
