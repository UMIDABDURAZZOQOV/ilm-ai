"""Digest-pinned original history content on the existing ILM assessment-v2 shape.

Inventory review never certifies claims. Exact source regions, fact review,
taught-card coverage and private MCQ/objective FRQ keys are required separately.
No external knowledge, database writes, translation, fuzzy grading or AI calls.
"""
from pathlib import Path
import re

from services.chemistry_grading import grade_answer, normalized_text
from services.world_history_validation import (
    DIRECTORY, fingerprint, load_catalog, read_json, require, require_complete_catalog,
)


def _read_indexed_pair(item):
    require(all(type(item.get(k)) is str and Path(item[k]).name == item[k]
                and '/' not in item[k] and '\\' not in item[k] for k in ('file', 'review_file')),
            'manifest_path_escape')
    lesson = read_json(DIRECTORY / item['file'])
    review = read_json(DIRECTORY / item['review_file'])
    require(fingerprint(lesson) == item.get('sha256') == review.get('lesson_sha256')
            and review.get('lesson_file') == item['file'], 'changed_content_requires_new_review')
    return lesson, review


def _prior_context(catalog, identifier, book_id, sequence, validated_prior):
    """Only already reviewed, earlier numbered units of this exact book.

    The normal ordered importer supplies its already validated prefix. Standalone
    validation resolves the same explicit index, never a filename inferred from
    a requested topic or an unreviewed catalogue presence record.
    """
    if validated_prior is not None:
        previous = validated_prior.get(identifier)
        require(previous is not None, 'context_requires_reviewed_predecessor')
    else:
        index = read_json(DIRECTORY / 'world_history_lessons.json')
        require(index.get('schema_version') == 1 and index.get('subject') == 'jahon_tarixi',
                'reviewed_index_required')
        matches = []
        for item in index.get('lessons', []):
            previous, prior_review = _read_indexed_pair(item)
            if previous.get('topic_id') == identifier:
                matches.append((previous, prior_review))
        require(len(matches) == 1, 'context_requires_unique_indexed_predecessor')
        previous, prior_review = matches[0]
        require(previous.get('book_id') == book_id and previous.get('sequence', sequence) < sequence,
                'context_requires_earlier_same_book_unit')
        validate_lesson(catalog, previous, prior_review)
    require(previous.get('book_id') == book_id and previous.get('sequence', sequence) < sequence,
            'context_requires_earlier_same_book_unit')
    return previous


def validate_lesson(catalog, lesson, review, *, _validated_prior=None):
    require_complete_catalog(catalog)
    require(lesson.get('schema_version') == 1 and lesson.get('assessment_version') == 2
            and lesson.get('subject') == 'jahon_tarixi' and lesson.get('language') == 'uz'
            and lesson.get('authorship') == 'original_fact_based_adaptation'
            and lesson.get('publication') == 'local_test_preview_only',
            'original_source_based_uzbek_history_lesson_required')
    book = next((b for b in catalog['books'] if b['id'] == lesson.get('book_id')), None)
    require(book is not None and lesson.get('grade') == book['grade'], 'lesson_book_mismatch')
    topic = next((t for t in book['teaching_units'] if t['id'] == lesson.get('topic_id')), None)
    require(topic is not None, 'catalogued_teaching_unit_required')
    require(lesson.get('sequence') == topic['sequence']
            and lesson.get('prerequisite_ids') == topic['prerequisite_ids']
            and lesson.get('title') == topic['title'], 'lesson_source_order_mismatch')
    revision = lesson.get('revision')
    require(type(revision) is int and revision >= 1
            and re.fullmatch(r'[a-z0-9-]{1,96}', lesson.get('key', '')), 'reviewed_lesson_key_required')
    require(review.get('schema_version') == 1 and review.get('original_authorship') is True
            and review.get('lesson_sha256') == fingerprint(lesson)
            and review.get('review_method') == 'original_page_images_and_embedded_text',
            'changed_content_requires_new_review')
    records = {r['id']: r for r in book['records'] + book['ancillary_records']}
    allowed = {topic['id']: records[topic['id']]}
    context = lesson.get('source_context_ids', [])
    require(type(context) is list and all(type(i) is str for i in context)
            and len(set(context)) == len(context), 'unique_source_context_required')
    previous_context = {}
    for identifier in context:
        record = records.get(identifier)
        require(record is not None and identifier not in allowed, 'linked_ancillary_context_required')
        if record['kind'] == 'numbered_topic':
            require(topic['kind'] in {'review', 'conclusion'}
                    and record['sequence'] < topic['sequence'],
                    'only_ancillary_review_can_reuse_earlier_numbered_context')
            previous_context[identifier] = _prior_context(
                catalog, identifier, book['id'], topic['sequence'], _validated_prior)
        else:
            require(topic['id'] in record.get('linked_teaching_ids', []),
                    'linked_ancillary_context_required')
        allowed[identifier] = record
    require(review.get('approved_context_sha256', {}) == {
        identifier: fingerprint(previous) for identifier, previous in previous_context.items()
    }, 'review_context_requires_exact_prior_lesson_digest')
    page_reviews = review.get('source_pages', [])
    require(type(page_reviews) is list and page_reviews, 'exact_page_review_required')
    pages = {p.get('review_id'): p for p in page_reviews}
    require(len(pages) == len(page_reviews) and None not in pages, 'unique_page_review_required')
    hashes = {p['pdf_page']: p['page_image_sha256'] for p in book['page_feature_inventory']}

    def source_refs(refs):
        require(type(refs) is list and refs, 'source_references_required')
        require(len({fingerprint(r) for r in refs}) == len(refs), 'duplicate_source_reference')
        for ref in refs:
            page = pages.get(ref.get('review_id'))
            record = allowed.get(ref.get('topic_id'))
            require(page and record and ref.get('verification') == page.get('verification')
                    == 'page_image_reviewed', 'original_claim_page_review_required')
            n = page.get('pdf_page')
            require(type(n) is int and n in record['pdf_pages'] and n == page.get('printed_page')
                    and page.get('page_image_sha256') == hashes.get(n), 'exact_original_page_digest_required')
            require(ref.get('book_id') == page.get('book_id') == book['id']
                    and ref.get('sha256') == page.get('sha256') == book['sha256']
                    and ref.get('file_name') == book['file_name']
                    and ref.get('book_title') == book['title'] and ref.get('authors') == book['authors']
                    and ref.get('year') == book['year'] and ref.get('grade') == book['grade']
                    and ref.get('topic_id') == page.get('topic_id') == record['id']
                    and ref.get('topic_title') == record['title'], 'claim_source_identity_mismatch')
            require(ref.get('chapter_id') == record.get('chapter_id')
                    and ref.get('paragraph') == (record.get('source_numbers') or [None])[0]
                    and ref.get('printed_pages') == [n] == ref.get('pdf_pages')
                    and ref.get('regions') == [page.get('region')]
                    and page.get('region') in {'topic_body', 'above_next_heading', 'below_topic_heading'},
                    'claim_page_region_mismatch')
            if record['kind'] == 'numbered_topic':
                overlaps = [r for r in book['records'] if n in r['pdf_pages'] and r['sequence'] > record['sequence']]
                if overlaps:
                    require(page['region'] == 'above_next_heading', 'shared_page_requires_exact_topic_region')
                previous = [r for r in book['records'] if n in r['pdf_pages'] and r['sequence'] < record['sequence']]
                if previous:
                    require(page['region'] == 'below_topic_heading', 'shared_opening_page_requires_topic_heading_scope')

    source_refs(lesson.get('source_refs'))
    facts = lesson.get('facts')
    require(type(facts) is dict and facts, 'reviewed_fact_ledger_required')
    require(review.get('approved_fact_sha256') == {i: fingerprint(f) for i, f in facts.items()},
            'every_fact_requires_explicit_review_digest')
    for identifier, fact in facts.items():
        require(fact.get('fact_id') == identifier and type(fact.get('claim')) is str and fact['claim']
                and fact.get('verification') == 'page_image_reviewed' and fact.get('review_note')
                and fact.get('claim_kind') in {'source_fact', 'textbook_periodization', 'attributed_textbook_interpretation'}
                and type(fact.get('automatic_assessment_allowed')) is bool,
                'reviewed_history_fact_required')
        require(type(fact.get('verified_answers')) is list and type(fact.get('approved_aliases')) is list
                and all(type(a) is str and a.strip() for a in fact['verified_answers'] + fact['approved_aliases']),
                'explicit_fact_answer_evidence_required')
        if fact['claim_kind'] == 'attributed_textbook_interpretation':
            require(not fact['automatic_assessment_allowed'], 'interpretation_requires_self_or_teacher_review')
        source_refs(fact.get('source_refs'))

    # A glossary lookup is a reference to already reviewed knowledge, not a new
    # approval of every meaning merely because a term occurs in the index.
    borrowed = {}
    bindings = review.get('approved_context_fact_bindings', {})
    require(type(bindings) is dict, 'review_context_fact_bindings_required')
    for identifier, fact in facts.items():
        origins = {ref['topic_id'] for ref in fact['source_refs']} & set(previous_context)
        if origins:
            require(len(origins) == 1 and {ref['topic_id'] for ref in fact['source_refs']} == origins,
                    'review_context_fact_must_retain_exact_origin')
            origin = next(iter(origins))
            binding = bindings.get(identifier, {})
            previous_fact = previous_context[origin]['facts'].get(binding.get('fact_id'))
            require(previous_fact is not None and binding == {
                'topic_id': origin, 'fact_id': previous_fact['fact_id'],
                'fact_sha256': fingerprint(previous_fact),
            }, 'review_context_fact_binding_mismatch')
            restored = dict(fact, fact_id=previous_fact['fact_id'])
            require(restored == previous_fact, 'review_context_cannot_change_prior_fact_or_assessment_scope')
            borrowed[identifier] = binding
    require(bindings == borrowed and set(previous_context) == {b['topic_id'] for b in borrowed.values()},
            'every_review_context_must_bind_exact_prior_facts')

    content = lesson.get('content', {})
    require(set(content) == {'cards', 'formulas', 'source_refs', 'xp_reward', 'reflections'}
            and content.get('formulas') == [] and type(content.get('xp_reward')) is int
            and content['xp_reward'] == 20, 'common_public_content_contract_required')
    require(review.get('approved_content_sha256') == fingerprint(content), 'changed_cards_require_review')
    require(content.get('source_refs') == lesson['source_refs'], 'public_bibliography_required')
    cards = content.get('cards')
    require(type(cards) is list and 1 <= len(cards) <= 24, 'bounded_theory_cards_required')
    taught = set()

    def fact_links(item, *, graded=False, exact_refs=True):
        ids = item.get('fact_ids', [])
        require(type(ids) is list and ids and all(type(i) is str and i in facts for i in ids)
                and len(ids) == len(set(ids)), 'known_unique_fact_links_required')
        if graded:
            require(set(ids) <= taught and all(facts[i]['automatic_assessment_allowed'] for i in ids),
                    'graded_question_must_use_taught_assessable_facts')
        source_refs(item.get('source_refs'))
        expected = {fingerprint(r) for i in ids for r in facts[i]['source_refs']}
        actual = {fingerprint(r) for r in item['source_refs']}
        require(expected == actual if exact_refs else expected <= actual, 'fact_citation_coverage_mismatch')
        return ids

    for card in cards:
        require(set(card) == {'title', 'body', 'fact_ids', 'source_refs'}
                and type(card.get('title')) is str and card['title']
                and type(card.get('body')) is str and 20 <= len(card['body']) <= 650,
                'short_original_theory_card_required')
        taught.update(fact_links(card))
    require(taught == set(facts), 'all_lesson_facts_must_be_taught')
    reflections = content.get('reflections')
    require(type(reflections) is list, 'reflection_list_required')
    for reflection in reflections:
        require(set(reflection) == {'title', 'body', 'grading', 'automatic_score', 'fact_ids', 'source_refs'}
                and reflection.get('grading') == 'self_or_teacher_review'
                and reflection.get('automatic_score') is False and reflection.get('body'),
                'open_historical_responses_cannot_be_automatically_graded')
        fact_links(reflection, exact_refs=False)
    assessments = lesson.get('assessments')
    require(type(assessments) is list and 2 <= len(assessments) <= 24
            and review.get('approved_assessments_sha256') == fingerprint(assessments),
            'explicit_reviewed_assessment_set_required')
    require(review.get('approved_answer_targets') == {
        q['key']: {'fact_ids': q['fact_ids'], 'verified_answer': q['grading_spec']['verified_answer'],
                   'aliases': q['grading_spec'].get('aliases', [])} for q in assessments
    }, 'question_specific_answer_target_review_required')
    keys, kinds = set(), set()
    for index, q in enumerate(assessments, 1):
        require(q.get('key') == f"{lesson['key']}-q{index:02d}" and q['key'] not in keys,
                'unique_ordered_assessment_keys_required')
        keys.add(q['key'])
        ids = fact_links(q, graded=True)
        kind, public, spec = q.get('response_kind'), q.get('public', {}), q.get('grading_spec', {})
        require(kind in {'concept_selection', 'short_text'} and spec.get('kind') == kind,
                'existing_objective_v2_response_kind_required')
        kinds.add(kind)
        require(type(public.get('prompt')) is str and public['prompt'], 'question_prompt_required')
        answers = {a for i in ids for a in facts[i]['verified_answers']}
        require(spec.get('verified_answer') in answers, 'answer_must_match_reviewed_fact')
        feedback = spec.get('feedback', {})
        require(feedback == {'correct': 'To‘g‘ri!', 'incorrect': 'Yana bir bor ko‘rib chiqamiz.',
                              'invalid_answer': 'Javobni ko‘rsatilgan shaklda kiriting.', 'answer_required': 'Avval javob kiriting.'},
                'generic_feedback_historical_explanation_belongs_in_cited_solution')
        solution = spec.get('solution', [])
        require(type(solution) is list and len(solution) == len(ids), 'cited_solution_required')
        for step, identifier in zip(solution, ids):
            require(step.get('body') == facts[identifier]['claim'] and step.get('fact_ids') == [identifier]
                    and step.get('source_refs') == facts[identifier]['source_refs'], 'solution_requires_exact_reviewed_fact')
        if kind == 'concept_selection':
            require(set(public) == {'prompt', 'options'}, 'public_mcq_must_not_expose_keys')
            options = public.get('options', [])
            require(type(options) is list and len(options) == 4
                    and all(set(o) == {'id', 'label'} and type(o['label']) is str and o['label'] for o in options),
                    'public_mcq_options_required')
            require([o['id'] for o in options] == spec.get('choice_ids')
                    and len({o['id'] for o in options}) == len(options)
                    and len({o['label'] for o in options}) == len(options), 'unique_mcq_choices_required')
            require(any(o['id'] == spec.get('expected') and o['label'] == spec['verified_answer'] for o in options),
                    'mcq_key_must_match_reviewed_answer')
            require(set(spec) == {'kind', 'expected', 'verified_answer', 'feedback', 'solution', 'choice_ids'},
                    'common_mcq_grading_spec_required')
            require(grade_answer(spec, {'choice_id': spec['expected']}) == 'correct', 'mcq_key_must_grade_correctly')
        else:
            require(set(public) == {'prompt', 'input_label', 'max_length'} and public['max_length'] == 80,
                    'public_frq_must_not_expose_rubric')
            require(set(spec) == {'kind', 'expected', 'verified_answer', 'feedback', 'solution', 'aliases'}
                    and spec.get('expected') == spec['verified_answer'], 'common_short_text_spec_required')
            aliases = spec.get('aliases', [])
            approved = {a for i in ids for a in facts[i]['approved_aliases']}
            require(type(aliases) is list and aliases and set(aliases) <= approved
                    and spec['expected'] in aliases
                    and len({normalized_text(a) for a in aliases}) == len(aliases),
                    'only_explicit_fact_reviewed_frq_aliases_allowed')
            require(all(grade_answer(spec, {'value': a}) == 'correct' for a in aliases), 'frq_alias_must_grade_correctly')
    require(kinds == {'concept_selection', 'short_text'}, 'mcq_and_suitable_objective_frq_required')
    activities = review.get('source_activity_coverage')
    require(type(activities) is list and activities, 'source_activity_coverage_review_required')
    activity_targets = ({f'card{i}' for i in range(1, len(cards)+1)}
                        | {f'q{i:02d}' for i in range(1, len(assessments)+1)}
                        | ({'reflection'} if reflections else set()))
    for activity in activities:
        require(activity.get('pdf_page') in {p['pdf_page'] for p in page_reviews}
                and activity.get('activity') and type(activity.get('covered_by')) is list
                and activity['covered_by'] and set(activity['covered_by']) <= activity_targets,
                'source_activity_must_resolve_to_reviewed_learning_content')
    return lesson


def load_lessons(catalog=None):
    catalog = require_complete_catalog(catalog or load_catalog())
    index = read_json(DIRECTORY / 'world_history_lessons.json')
    require(index.get('schema_version') == 1 and index.get('subject') == 'jahon_tarixi', 'reviewed_index_required')
    lessons, topics, keys = [], set(), set()
    validated_prior = {}
    for item in index.get('lessons', []):
        lesson, review = _read_indexed_pair(item)
        validate_lesson(catalog, lesson, review, _validated_prior=validated_prior)
        require(lesson['topic_id'] not in topics and lesson['key'] not in keys,
                'duplicate_reviewed_lesson')
        require(set(lesson['prerequisite_ids']) <= topics, 'missing_reviewed_prerequisite')
        topics.add(lesson['topic_id'])
        keys.add(lesson['key'])
        lessons.append(lesson)
        validated_prior[lesson['topic_id']] = lesson
    return lessons
