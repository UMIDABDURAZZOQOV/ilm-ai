"""Normal mobile contracts composed over reviewed engines, opt-in staging only."""
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from pydantic import ConfigDict, ValidationError
from sqlalchemy.orm import Session

from services import beta_curriculum as beta
from services.auth_deps import get_authenticated_user_id, verify_user_access
from services.db import get_db
from services.mobile_publication import mobile_publication
from services.models import User, UserStudyPreferences
from routers import skills, physics_preview, chemistry_preview, world_history_preview, uzbekistan_history_preview


def beta_db(db: Session = Depends(get_db)):
    beta.gate(db)
    return db


router = APIRouter(prefix='/beta', dependencies=[Depends(beta_db)])
DB = Annotated[Session, Depends(beta_db)]
UID = Annotated[int, Depends(get_authenticated_user_id)]
OWNER = Annotated[int, Depends(verify_user_access)]
bio_scope = asynccontextmanager(mobile_publication)
SCHEMAS = dict(fizika=physics_preview, kimyo=chemistry_preview,
               jahon_tarixi=world_history_preview, ozbekiston_tarixi=uzbekistan_history_preview)


@router.get('/skills/subjects')
async def subjects(request: Request, db: DB, grade: int | None = None):
    if grade is not None and grade not in range(5,12):
        raise HTTPException(422, 'grade_out_of_range')
    async with bio_scope(request, db):
        bio_grades = skills.list_curriculum_grades('biologiya', db)['grades']
    result = []
    for slug in beta.SUBJECTS:
        rows = bio_grades if slug == 'biologiya' else beta.grades(db, slug)['grades']
        available_grades = [g['grade'] for g in rows if g['ready_lessons'] > 0]
        if grade is None or grade in available_grades:
            result.append(dict(beta.metadata(slug), grades=available_grades,
                               ready_lessons=sum(g['ready_lessons'] for g in rows)))
    for slug, names in [('matematika', ('Matematika', 'Математика', 'Mathematics')),
                        ('ona_tili', ('Ona tili', 'Родной язык', 'Native language'))]:
        result.append(dict(id=-len(result)-1, slug=slug, name_uz=names[0], name_ru=names[1], name_en=names[2],
                           color='#8D879F', icon='menu_book', grades=[], available=False, ready_lessons=0))
    return result


@router.get('/skills/subjects/{subject_slug}/grades')
async def grades(subject_slug: str, request: Request, db: DB):
    if subject_slug == 'biologiya':
        async with bio_scope(request, db):
            return skills.list_curriculum_grades(subject_slug, db)
    return beta.grades(db, subject_slug)


@router.get('/skills/{user_id}/tree')
async def tree(subject: str, grade: int, request: Request, db: DB, user_id: OWNER):
    if subject == 'biologiya':
        async with bio_scope(request, db):
            return skills.get_tree(subject, grade, user_id, db)
    return beta.tree(db, user_id, subject, grade)


@router.get('/skills/{user_id}/curriculum')
async def outline(subject: str, grade: int, request: Request, db: DB, user_id: OWNER):
    if subject == 'biologiya':
        async with bio_scope(request, db):
            return skills.get_curriculum(subject, grade, user_id, db)
    return beta.outline(db, user_id, subject, grade)


@router.get('/skills/{user_id}/profile')
async def profile(request: Request, db: DB, user_id: OWNER):
    async with bio_scope(request, db):
        result = skills.get_profile(user_id, db)
    return beta.append_progress(db, user_id, result)


@router.get('/skills/{user_id}/preferences')
def preferences(db: DB, user_id: OWNER):
    return skills.get_study_preferences(user_id, db)


class Preferences(skills.StudyPreferencesRequest):
    model_config = ConfigDict(extra='forbid')


@router.post('/skills/{user_id}/preferences')
def save_preferences(data: Preferences, db: DB, user_id: OWNER):
    values = data.model_dump(exclude_unset=True, exclude_none=True)
    if values.get('subject') is not None and values['subject'] not in beta.SUBJECTS:
        raise HTTPException(422, 'subject_not_available')
    if values.get('grade') is not None and values['grade'] not in ['all', *map(str, range(5,12))]:
        raise HTTPException(422, 'grade_out_of_range')
    if 'daily_goal_xp' in values and values['daily_goal_xp'] not in (10,20,30,50):
        raise HTTPException(422, 'invalid_daily_goal')
    if 'level' in values and values['level'] not in range(1,6):
        raise HTTPException(422, 'invalid_level')
    if any(isinstance(v,str) and len(v) > (500 if k=='reason' else 100) for k,v in values.items()):
        raise HTTPException(422, 'preference_too_long')
    if db.query(User).filter_by(id=user_id).with_for_update().first() is None:
        raise HTTPException(404, 'user_not_found')
    row = db.get(UserStudyPreferences, user_id)
    if row is None:
        row = UserStudyPreferences(user_id=user_id)
        db.add(row)
    for field, value in values.items():
        setattr(row, field, value)
    db.commit()
    return {'preferences': skills._preference_payload(row)}


def validated(slug, operation, data):
    if slug not in SCHEMAS:
        raise HTTPException(404, 'subject_not_available')
    model = getattr(SCHEMAS[slug], operation)
    try:
        return model.model_validate(data)
    except ValidationError:
        raise HTTPException(422, 'invalid_assessment_request') from None


@router.get('/v2/{subject}/catalog')
def catalog(subject: str, db: DB, uid: UID, grade: int):
    result = beta.adapter(db,subject)[0].catalog(db,uid,grade)
    fields = ('id','title','authors','publisher','year','edition','file_name')
    result['source_books'] = [{k:book[k] for k in fields if k in book} for book in
        (beta.book(subject,g['grade']) for g in beta.grades(db,subject)['grades'])]
    return result


@router.post('/v2/{subject}/lessons/{key}/start')
def start(subject: str, key: str, db: DB, uid: UID, data: dict = Body(...)):
    runtime = beta.adapter(db, subject)[0]
    parsed = validated(subject, 'Start', data)
    result = runtime.start(db, uid, key, str(parsed.request_id))
    # Preserve all public teaching sections from the immutable issued snapshot.
    # Older History preview responses omitted examples/formulas from their view.
    # Never copy the session's assessments/grading specs into a public response.
    from copy import deepcopy
    from services.models import StudySession
    snapshot = db.get(StudySession,result['attempt_id']).questions['content']
    result = dict(result, content=dict(result['content'], **{
        field:deepcopy(snapshot.get(field,[])) for field in ('cards','formulas','examples','reflections')}))
    if result.get('result') is not None:
        result = dict(result, result=completion_presentation(db, result['result']))
    return result


@router.post('/v2/{subject}/attempts/{sid}/answers')
def answer(subject: str, sid: str, db: DB, uid: UID, data: dict = Body(...)):
    runtime = beta.adapter(db, subject)[0]
    parsed = validated(subject, 'Submission', data)
    return runtime.submit(db, uid, sid, parsed.assessment_key, parsed.answer.model_dump(exclude_none=True))


@router.post('/v2/{subject}/attempts/{sid}/complete')
def complete(subject: str, sid: str, db: DB, uid: UID, data: dict = Body(...)):
    runtime = beta.adapter(db, subject)[0]
    validated(subject, 'Completion', data)
    return completion_presentation(db, runtime.complete(db, uid, sid))


def completion_presentation(db, result):
    from services.models import StudySession
    from services.study import aware
    row = db.get(StudySession, result['attempt_id'])
    pct = result['score_pct']
    return dict(result, stars=3 if pct >= 90 else 2 if pct >= 80 else 1 if pct >= 60 else 0,
                elapsed_seconds=max(0, int((aware(row.completed_at)-aware(row.started_at)).total_seconds())))


# Existing Biology lessons/practice/quests/league/summary keep the original
# reviewed mobile publication policy. Explicit integration routes above win.
router.include_router(skills.router, dependencies=[Depends(mobile_publication)])
