"""Integrated beta presentation over the existing five reviewed runtimes.

No content generation, copied answer keys, progress migration or publication.
Every v2 action still passes the original runtime's preview/source/DB gates.
"""
import hashlib
import json
import os
from functools import lru_cache
from pathlib import Path

from fastapi import HTTPException
from sqlalchemy import func

from services import assessment_runtime, chemistry_runtime, world_history_runtime, uzbekistan_history_runtime
from services.assessment_models import CurriculumLessonV2, AssessmentV2Progress
from services.chemistry_models import ChemistryLesson, ChemistryProgress
from services.world_history_models import WorldHistoryLesson, WorldHistoryProgress
from services.uzbekistan_history_models import HistoryLesson, HistoryProgress
from services.models import User

ROOT = Path(__file__).resolve().parents[1] / 'scripts/curriculum'
SUBJECTS = {
    'biologiya': ('Biologiya', 'Биология', 'Biology', '#22A888', 'eco'),
    'fizika': ('Fizika', 'Физика', 'Physics', '#6C55D9', 'bolt'),
    'kimyo': ('Kimyo', 'Химия', 'Chemistry', '#DE9638', 'science'),
    'ozbekiston_tarixi': ('O‘zbekiston tarixi', 'История Узбекистана', 'Uzbekistan History', '#C46B5D', 'history_edu'),
    'jahon_tarixi': ('Jahon tarixi', 'Всемирная история', 'World History', '#478CC8', 'public'),
}
ADAPTERS = {
    'fizika': (assessment_runtime, CurriculumLessonV2, AssessmentV2Progress, 'physics/physics_sources.json'),
    'kimyo': (chemistry_runtime, ChemistryLesson, ChemistryProgress, 'chemistry/chemistry_sources.json'),
    'jahon_tarixi': (world_history_runtime, WorldHistoryLesson, WorldHistoryProgress, 'world_history/world_history_sources.json'),
    'ozbekiston_tarixi': (uzbekistan_history_runtime, HistoryLesson, HistoryProgress, 'uzbekistan_history/sources.json'),
}


def gate(db):
    url = db.get_bind().url
    owned = (url.get_backend_name() == 'sqlite' and 'beta_staging' in (url.database or '')) or (
        url.get_backend_name() == 'postgresql' and url.host in {'127.0.0.1', 'localhost', '::1'}
        and 'staging' in (url.database or ''))
    if os.getenv('ILM_BETA_ENABLED') != 'true' or os.getenv('ENVIRONMENT') not in {'test', 'development'} or not owned:
        raise HTTPException(404, 'integrated_beta_disabled')


def adapter(db, slug):
    if slug not in ADAPTERS:
        raise HTTPException(404, 'subject_not_available')
    item = ADAPTERS[slug]
    from services.reviewed_mobile_release import authorized
    if not authorized(db, slug):
        item[0].preview_gate(db)
    return item


def metadata(slug):
    names = SUBJECTS[slug]
    return dict(id=list(SUBJECTS).index(slug)+1, slug=slug, name_uz=names[0], name_ru=names[1],
                name_en=names[2], color=names[3], icon=names[4], available=True)


@lru_cache(maxsize=32)
def book(slug, grade):
    data = json.loads((ROOT / ADAPTERS[slug][3]).read_text(encoding='utf8'))
    result = next((b for b in data['books'] if b['grade'] == grade), None)
    if result is None:
        raise HTTPException(404, 'grade_not_available')
    return result


def grades(db, slug):
    runtime, model, _, _ = adapter(db, slug)
    return {'subject': slug, 'grades': [dict(grade=grade, title_uz=book(slug, grade)['title'],
        status='mapped', ready_lessons=count, language='uz') for grade, count in
        db.query(model.grade, func.count(model.key)).filter_by(subject=slug).group_by(model.grade).order_by(model.grade)]}


def chapter_metadata(slug, grade):
    source = book(slug, grade)
    rows = source.get('chapters', []) + source.get('records', []) + source.get('topics', []) + source.get('ancillary_records', [])
    records = {r['id']: r for r in rows}
    # Some verified books have numbered topics but no chapter headings. A book
    # container is presentation metadata, never an invented textbook chapter.
    records['__book__'] = dict(id='__book__',title=source['title'],kind='book')
    return records


def tree(db, uid, slug, grade):
    runtime, model, _, _ = adapter(db, slug)
    if grade not in [g['grade'] for g in grades(db, slug)['grades']]:
        raise HTTPException(404, 'grade_not_available')
    catalog = runtime.catalog(db, uid, grade)
    lessons = {r.key: r for r in runtime.lessons(db, grade)}
    chapters = chapter_metadata(slug, grade)
    units = {}
    ids = set()
    for entry in catalog['lessons']:
        row = lessons[entry['key']]
        refs = row.content['source_refs']
        record = chapters.get(row.topic_id, {})
        chapter = record.get('chapter_id') or refs[0].get('chapter_id')
        if chapter is None and record.get('kind') in {'introduction','conclusion','review','glossary'}:
            chapter = row.topic_id
        if chapter is None and not book(slug,grade).get('chapters') and record:
            chapter = '__book__'
        if chapter not in chapters:
            raise HTTPException(503, 'reviewed_chapter_metadata_missing')
        # Stable presentation IDs only; the real action always uses the opaque key.
        ident = -int(hashlib.sha256(row.key.encode()).hexdigest()[:12], 16)
        if ident in ids:
            raise HTTPException(503, 'presentation_identifier_collision')
        ids.add(ident)
        if chapter not in units:
            title = chapters[chapter]['title']
            units[chapter] = dict(id=-len(units)-1, slug=chapter, title_uz=title, title_ru=title,
                title_en=title, order_index=len(units)+1, exam={'status': 'none'},
                coverage_complete=True, lessons=[])
        score = entry.get('best_score_pct') or 0
        units[chapter]['lessons'].append(dict(id=ident, slug=row.key, assessment_key=row.key,
            assessment_subject=slug, grade=grade, title_uz=row.title, title_ru=row.title, title_en=row.title,
            order_index=row.sequence, xp_reward=row.content.get('xp_reward', 10 if slug in {'fizika', 'ozbekiston_tarixi'} else 20),
            status={'available':'unlocked'}.get(entry['state'], entry['state']),
            stars=(3 if score >= 90 else 2 if score >= 80 else 1 if score >= 60 else 0),
            best_score_pct=score, source_refs=refs))
    from routers.skills import _gamification_block
    user = db.get(User, uid)
    if user is None:
        raise HTTPException(404, 'user_not_found')
    return dict(subject=metadata(slug), units=list(units.values()), user=_gamification_block(user, db))


def outline(db, uid, slug, grade):
    path = tree(db, uid, slug, grade)
    def source(lesson):
        pages = [page for ref in lesson['source_refs'] for page in ref['printed_pages']]
        return dict(printed_start=min(pages), printed_end=max(pages)) if pages else {}
    chapters = [dict(title_uz=u['title_uz'], topics=[dict(title_uz=lesson['title_uz'], kind='topic',
        ready=True, completed=lesson['status']=='completed', source=source(lesson)) for lesson in u['lessons']]) for u in path['units']]
    done = bool(chapters) and all(t['completed'] for c in chapters for t in c['topics'])
    next_grade = next((g['grade'] for g in grades(db, slug)['grades'] if g['grade'] > grade), None)
    return dict(chapters=chapters, completed=done, next_grade=next_grade if done else None)


def append_progress(db, uid, profile):
    subjects = profile['subjects']
    for slug in ADAPTERS:
        # Use the same capability-checked adapter as tree/start/answer routes.
        # Reviewed publication retains its authorization; local previews still
        # have to pass their original runtime gate.
        _, model, progress, _ = adapter(db, slug)
        total = db.query(model).filter_by(subject=slug).count()
        completed, stars = 0, 0
        for row in db.query(progress).join(model, model.key == progress.lesson_key).filter(progress.user_id == uid, model.subject == slug):
            if row.completed_at is not None:
                completed += 1
                stars += 3 if row.best_score_pct >= 90 else 2 if row.best_score_pct >= 80 else 1
        subjects.append(dict(metadata(slug), total=total, completed=completed, stars=stars,
                             pct=round(completed/total*100) if total else 0))
    profile['lessons_completed'] = sum(s['completed'] for s in subjects)
    done = [s for s in subjects if s['completed']]
    profile['strongest'] = max(done, key=lambda s:s['pct'], default=None)
    profile['weakest'] = min(done, key=lambda s:s['pct'], default=None)
    return profile


def append_achievements(db, uid, payload):
    """Include reviewed completions without awarding XP or rewriting progress.

    Legacy tiers cap their progress at each target. The largest tier preserves
    enough of the legacy count to calculate every existing target after adding
    the reviewed counts. A completed progress row counts once, including replays.
    Question totals follow the legacy rule: every completed attempt counts.
    """
    from services.models import StudySession

    extra = dict(lessons=0, perfect=0, questions=0)
    kinds = []
    for slug in ADAPTERS:
        runtime, model, progress, _ = adapter(db, slug)
        kinds.append(runtime.KIND)
        rows = db.query(progress.best_score_pct).join(
            model, model.key == progress.lesson_key
        ).filter(progress.user_id == uid, model.subject == slug,
                 progress.completed_at.isnot(None)).all()
        extra['lessons'] += len(rows)
        extra['perfect'] += sum(score is not None and score >= 90 for (score,) in rows)
    for (response,) in db.query(StudySession.response).filter(
        StudySession.user_id == uid, StudySession.kind.in_(kinds),
        StudySession.completed_at.isnot(None)
    ):
        total = response.get('total') if isinstance(response, dict) else None
        if type(total) is int and total >= 0:
            extra['questions'] += total

    result = dict(payload, achievements=[dict(a) for a in payload['achievements']])
    for group, added in extra.items():
        tiers = [a for a in result['achievements'] if a['group'] == group]
        value = max((a['progress'] for a in tiers), default=0) + added
        for achievement in tiers:
            achievement.update(progress=min(value, achievement['target']),
                               earned=value >= achievement['target'])
    return result
