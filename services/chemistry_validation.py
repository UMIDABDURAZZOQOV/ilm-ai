"""Pure Chemistry evidence validation. No ORM, DB, network or LLM imports.

Keep Biology's validator and Physics's unfinished preview untouched. Catalogue
mapping is distinct from scientific claim review and executable lesson readiness.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "scripts/curriculum/chemistry"
SOURCE_PATH = DIRECTORY / "chemistry_sources.json"
PINNED_SOURCES = {
    7: ("a164c51ca0f55b8024e74d8e6daa32a3b10a3d45b33761630add81c47e24ce0a", 81, 51, 6, 16, 7),
    8: ("077e2c96380950d3dd4118489474a200a08d39ff226b7096dd48436df9bc8056", 208, 44, 6, 10, 5),
    9: ("ee3695eeb0598016629cc370dfcb0c73836250cf594f4d5d0cb2a06ea40c7386", 208, 41, 5, 17, 3),
    10: ("b9edd182161159f109fbbb668bc1656e00e221aab9411ec83b16ff1889244cb6", 160, 35, 4, 6, 0),
    11: ("ee3d429585691951eb0f5529553f5879869cd084e1886e01b950d6971cf2952b", 160, 33, 8, 0, 0),
}
PINNED_IDENTITIES = {
    7: ('chemistry-7-uz-2017', 'kimyo_7_uzb.pdf'),
    8: ('chemistry-8-uz-2019', 'kimyo_8_uzb.pdf'),
    9: ('chemistry-9-uz-2019', 'kimyo_9_uzb.pdf'),
    10: ('chemistry-10-uz-2017', 'organik_kimyo_10_uzb.pdf'),
    11: ('chemistry-11-uz-2018', 'umumiy_kimyo_11_uzb.pdf'),
}
TEACHING_KINDS = {"paragraph", "laboratory", "practical"}
HEADING_STATES = {"body_text_heading_verified", "body_image_heading_verified"}
KNOWN_SOURCE_HOLDS = {'ch9-paragraph40': 'ch9-p40-page186-configuration-conflict'}
KNOWN_EDITORIAL_ISSUES = {
    'ch7-paragraph13': 'ch7-p13-p41-percentage-discrepancy',
    'ch7-paragraph18': 'ch7-p18-ozone-context-review',
    'ch7-paragraph19': 'ch7-p19-silane-equation-review',
    'ch7-paragraph20': 'ch7-p20-photosynthesis-label-review',
    'ch7-paragraph24': 'ch7-p24-heat-sign-review',
    'ch7-paragraph26': 'ch7-p26-environmental-scope-review',
    'ch7-4': 'ch7-review3-gas-phase-context',
    'ch7-paragraph27': 'ch7-p27-water-condition-review',
    'ch7-paragraph28': 'ch7-p28-ocean-volume-discrepancy',
    'ch7-practical05': 'ch7-practical5-universal-colour-review',
    'ch7-7': 'ch7-review4-water-vapour-state',
    'ch7-paragraph33': 'ch7-p33-francium-state-review',
    'ch7-paragraph34': 'ch7-p34-iron-percentage-precision',
    'ch7-paragraph37': 'ch7-p37-occurrence-mineral-review',
    'ch9-paragraph27': 'ch9-p27-gem-and-equation-review',
    'ch7-paragraph42': 'ch7-p42-acid-notation-valence-review',
    'ch7-paragraph43': 'ch7-p43-basicity-scope-review',
    'ch7-paragraph44': 'ch7-p44-product-scope-review',
    'ch7-paragraph45': 'ch7-p45-condition-scope-review',
    'ch7-paragraph46': 'ch7-p46-legacy-iodide-review',
    'ch7-paragraph48': 'ch7-p48-copper-iodide-review',
    'ch7-paragraph49': 'ch7-p49-medical-current-scope-review',
    'ch7-paragraph50': 'ch7-p50-gas-precision-context-review',
}
UNRESOLVED_PERCENTAGES = re.compile(r'(?<![0-9])(?:42[.,](?:88|86)|57[.,](?:12|14)|27[.,](?:29|27)|72[.,](?:71|73))(?![0-9])')


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode()).hexdigest()


def page_locator(grade, printed):
    if type(printed) is not int or printed < 1:
        raise ValueError("invalid_printed_page")
    if grade != 7:
        return {"pdf_page": printed, "region": "full"}
    if printed in {1, 160}:
        return {"pdf_page": 1 if printed == 1 else 81, "region": "full"}
    if printed > 160:
        raise ValueError("invalid_printed_page")
    return {"pdf_page": printed // 2 + 1,
            "region": "left" if printed % 2 == 0 else "right"}


def validate_catalog(catalog):
    if (catalog.get("schema_version") != 1 or catalog.get("subject_slug") != "kimyo"
            or catalog.get("language") != "uz"):
        raise ValueError("unsupported_chemistry_catalog")
    books = catalog.get("books", [])
    if sorted(b.get("grade", 0) for b in books) != list(range(7, 12)):
        raise ValueError("five_unique_chemistry_grades_required")
    all_ids = set()
    for book in books:
        grade = book["grade"]
        digest, pages, paras, chapters, labs, practicals = PINNED_SOURCES[grade]
        if (book.get('id'),book.get('file_name')) != PINNED_IDENTITIES[grade]:
            raise ValueError('pinned_source_identity_required')
        if (book.get("sha256") != digest or book.get("pdf_page_count") != pages
                or book.get("decoded_pages") != pages or book.get("source_status") != "mapped"):
            raise ValueError("unreviewed_source_identity_or_page_count")
        if (book.get("bibliography_review", {}).get("status") != "page_images_reviewed"
                or book.get("toc_review", {}).get("status") != "page_images_reviewed"):
            raise ValueError("source_image_review_required")
        if book.get("rights", {}).get("fulltext_republication") != "not_authorized":
            raise ValueError("source_rights_required")
        records = book.get("records", [])
        ids = {r["id"] for r in records}
        if len(ids) != len(records) or ids & all_ids:
            raise ValueError("duplicate_source_record")
        all_ids |= ids
        for kind, count in [("paragraph", paras), ("chapter", chapters),
                            ("laboratory", labs), ("practical", practicals)]:
            numbers = sorted(r["number"] for r in records if r["kind"] == kind)
            if numbers != list(range(1, count + 1)):
                raise ValueError("source_coverage_gap_or_duplicate")
        instructional = [r for r in records if r["kind"] in TEACHING_KINDS]
        for i, record in enumerate(instructional):
            expected = [instructional[i-1]["id"]] if i else []
            if record.get("sequence") != i+1 or record.get("prerequisite_ids") != expected:
                raise ValueError("source_prerequisite_order_mismatch")
        starts = [r["printed_start"] for r in records]
        if starts != sorted(starts):
            raise ValueError("source_order_changed")
        for r in records:
            if r['id'] in KNOWN_EDITORIAL_ISSUES:
                require(any(i.get('id') == KNOWN_EDITORIAL_ISSUES[r['id']]
                            and i.get('status') == 'open_review'
                            for i in r.get('editorial_review_issues', [])),
                        'known_editorial_issue_must_remain_visible')
            if r['id'] in KNOWN_SOURCE_HOLDS and (
                    r.get('source_review_hold',{}).get('id') != KNOWN_SOURCE_HOLDS[r['id']]
                    or r.get('source_review_hold',{}).get('status') != 'open'
                    or r.get('fact_review_status') != 'blocked_source_conflict'):
                raise ValueError('known_source_conflict_must_remain_on_review_hold')
            if (r.get("source_id") != book["id"] or r.get("source_sha256") != digest
                    or r.get("source_file") != book["file_name"]):
                raise ValueError("record_source_identity_mismatch")
            if not 1 <= r["printed_start"] <= r["printed_end"] <= book["printed_page_count"]:
                raise ValueError("invalid_source_page_range")
            for name, field in [("start_locator", "printed_start"), ("end_locator", "printed_end")]:
                if r.get(name) != page_locator(grade, r[field]):
                    raise ValueError("printed_pdf_region_mapping_mismatch")
            state = r.get("heading_review", {}).get("status")
            if state not in HEADING_STATES or (grade >= 10 and state != "body_image_heading_verified"):
                raise ValueError("unreviewed_or_ocr_only_heading")
            if r["kind"] in TEACHING_KINDS and r.get("chapter_id") not in ids:
                raise ValueError("missing_source_container")
            if r.get("parent_id") and r["parent_id"] not in ids:
                raise ValueError("missing_source_parent")
            if r["kind"] in {"laboratory", "practical", "subactivity"}:
                if r.get("digital_activity_policy") != {
                    "mode": "guided_analysis", "physical_execution_required": False,
                    "real_lab_certification": False,
                }:
                    raise ValueError("digital_lab_policy_required")
    return catalog


def load_catalog():
    return validate_catalog(read_json(SOURCE_PATH))


def source_review_issues(book):
    return [issue['id'] for r in book['records'] for issue in
            ([r['source_review_hold']] if r.get('source_review_hold', {}).get('status') == 'open' else [])
            + [i for i in r.get('editorial_review_issues', []) if i.get('status') == 'open_review']]


def readiness(catalog, lessons=()):
    ready = {lesson["topic_id"] for lesson in lessons}
    result = []
    for book in catalog["books"]:
        rows = [r for r in book["records"] if r["kind"] in TEACHING_KINDS]
        issues = source_review_issues(book)
        result.append({"grade": book["grade"], "chapters": book["chapter_count"],
                       "paragraphs": book["paragraph_count"],
                       "laboratories": book["laboratory_count"],
                       "practicals": book["practical_count"],
                       "source_teaching_entries": len(rows),
                       "implemented_lessons": sum(r["id"] in ready for r in rows),
                       "remaining_ids": [r["id"] for r in rows if r["id"] not in ready],
                       "pending_source_review_ids": issues,
                       "source_review_complete": not issues,
                       "course_ready": all(r["id"] in ready for r in rows) and not issues})
    return result


def require(condition, code):
    if not condition:
        raise ValueError(code)


def validate_lesson(catalog, lesson, review):
    """Validate evidence/content shape, taught facts and deterministic keys."""
    from services.chemistry_grading import normalized_text, grade_answer

    def copy_integrity(value):
        if isinstance(value, str):
            require('\ufffd' not in value and not re.search(r'[A-Za-z]\?[A-Za-z]', value),
                    'corrupted_utf8_lesson_copy')
        elif isinstance(value, dict):
            for child in value.values():
                copy_integrity(child)
        elif isinstance(value, list):
            for child in value:
                copy_integrity(child)

    copy_integrity(lesson)

    validate_catalog(catalog)
    require(lesson.get("schema_version") == 1 and lesson.get("assessment_version") == 2
            and lesson.get("subject") == "kimyo" and lesson.get("language") == "uz"
            and lesson.get("authorship") == "original_fact_based_adaptation"
            and lesson.get("publication") == "local_test_preview_only",
            "original_source_based_uzbek_lesson_required")
    book = next((b for b in catalog["books"] if b["id"] == lesson["book_id"]), None)
    require(book is not None and lesson["grade"] == book["grade"], "lesson_book_mismatch")
    topic = next((r for r in book["records"] if r["id"] == lesson["topic_id"]), None)
    require(topic and topic["kind"] in TEACHING_KINDS, "source_topic_required")
    require(topic['id'] not in KNOWN_SOURCE_HOLDS and
            topic.get('source_review_hold',{}).get('status') != 'open',
            'unresolved_source_review_issue')
    require(lesson.get("sequence") == topic["sequence"] and
            lesson.get("prerequisite_ids") == topic["prerequisite_ids"], "lesson_order_mismatch")
    require(type(lesson.get("revision")) is int and lesson["revision"] > 0,
            "positive_reviewed_revision_required")
    records = {r['id']: r for r in book['records']}
    allowed_sources = {topic['id']: topic}
    for field in ('source_context_ids', 'source_activity_ids'):
        linked = lesson.get(field, [])
        require(type(linked) is list and all(type(x) is str for x in linked)
                and len(linked) == len(set(linked)),
                'explicit_unique_source_links_required')
        for identifier in linked:
            record = records.get(identifier)
            require(record and identifier not in allowed_sources
                    and identifier not in KNOWN_SOURCE_HOLDS
                    and record.get('source_review_hold', {}).get('status') != 'open',
                    'unknown_or_blocked_linked_source')
            if field == 'source_context_ids':
                if record['kind'] == 'review':
                    predecessors = [r['sequence'] for r in book['records'] if r['kind'] in TEACHING_KINDS
                                    and r['chapter_id'] == record['chapter_id']
                                    and r['printed_start'] <= record['printed_start']]
                    require(predecessors and max(predecessors) < topic['sequence']
                            and record['printed_end'] <= topic['printed_start'],
                            'source_context_must_precede_lesson')
                else:
                    require(record['kind'] in TEACHING_KINDS and record['sequence'] < topic['sequence'],
                            'source_context_must_precede_lesson')
            else:
                require(record['kind'] == 'review' and record['chapter_id'] == topic['chapter_id'],
                        'same_chapter_review_anchor_required')
                predecessors = [r['sequence'] for r in book['records'] if r['kind'] in TEACHING_KINDS
                                and r['chapter_id'] == record['chapter_id']
                                and r['printed_start'] <= record['printed_start']]
                require(predecessors and max(predecessors) == topic['sequence'],
                        'chapter_review_belongs_to_last_preceding_lesson')
            allowed_sources[identifier] = record
    pages = {p["review_id"]: p for p in review.get("source_pages", [])}
    require(pages and len(pages) == len(review["source_pages"]), "unique_page_review_required")

    def source_refs(refs):
        require(type(refs) is list and refs, "source_references_required")
        for ref in refs:
            evidence = pages.get(ref.get("review_id"))
            cited = allowed_sources.get(ref.get('topic_id'))
            require(evidence and evidence.get("verification") == "page_image_reviewed"
                    and ref.get("verification") == "page_image_reviewed"
                    and re.fullmatch(r"[0-9a-f]{64}", evidence.get("page_image_sha256", "")),
                    "original_page_image_review_required")
            require(ref.get("book_id") == book["id"] == evidence["book_id"]
                    and ref.get("sha256") == book["sha256"] == evidence["sha256"]
                    and ref.get("file_name") == book["file_name"]
                    and cited and ref.get("topic_id") == cited["id"] == evidence["topic_id"]
                    and ref.get("paragraph") == cited["number"], "claim_source_identity_mismatch")
            require(ref.get('book_title') == book['title'] and ref.get('authors') == book['authors']
                    and ref.get('year') == book['year'] and ref.get('topic_title') == cited['title'],
                    'claim_bibliography_mismatch')
            pp = ref.get("printed_pages", [])
            require(pp == [evidence["printed_page"]] and
                    cited["printed_start"] <= pp[0] <= cited["printed_end"], "claim_outside_topic")
            loc = page_locator(book["grade"], pp[0])
            require(ref.get("pdf_pages") == [loc["pdf_page"]] == [evidence["pdf_page"]]
                    and ref.get("regions") == [loc["region"]] == [evidence["region"]],
                    "claim_pdf_printed_region_mismatch")

    source_refs(lesson.get("source_refs"))
    facts = lesson.get("facts", {})
    require(type(facts) is dict and facts, "reviewed_facts_required")
    for f in facts.values():
        require(type(f.get("claim")) is str and f["claim"] and f.get("verified_answers")
                and all(type(a) is str and a for a in f["verified_answers"]), "fact_answer_evidence_required")
        source_refs(f.get("source_refs"))
        if any(r['topic_id'] == 'ch7-paragraph13' for r in f['source_refs']):
            require(not any(UNRESOLVED_PERCENTAGES.search(a) for a in f['verified_answers']),
                    'unresolved_source_percentage_cannot_be_an_answer')
        if any(r['topic_id'] == 'ch7-paragraph19' for r in f['source_refs']):
            require(not any('SiH4' in a or 'SiH₄' in a for a in f['verified_answers']),
                    'unresolved_silane_equation_cannot_be_an_answer')
        if any(r['topic_id'] == 'ch7-paragraph20' for r in f['source_refs']):
            require(not any('*' in a for a in f['verified_answers']),
                    'unresolved_photosynthesis_label_cannot_be_an_answer')
        if any(r['topic_id'] == 'ch7-4' for r in f['source_refs']):
            require(not any(a in {'S8', 'S₈', '0.89', '0,89'} for a in f['verified_answers']),
                    'unresolved_gas_phase_cannot_be_an_answer')
        if any(r['topic_id'] == 'ch7-paragraph28' for r in f['source_refs']):
            from services.chemistry_grading import canonical_number
            for answer in f['verified_answers']:
                try:
                    value = canonical_number(answer)
                except ValueError:
                    continue
                require(value not in {'1350000', '1400000000'},
                        'unresolved_ocean_volume_cannot_be_an_answer')
        if any(r['topic_id'] == 'ch7-practical05' for r in f['source_refs']):
            require(not any(a.casefold() == 'pushti' for a in f['verified_answers']),
                    'unresolved_soil_universal_colour_cannot_be_an_answer')
        if any(r['topic_id'] == 'ch7-paragraph34' for r in f['source_refs']):
            require(not any(re.search(r'(?<![0-9])(?:72[.,]2|27[.,]8)(?![0-9])', a)
                            for a in [f['claim'], *f['verified_answers']]),
                    'unresolved_iron_percentage_cannot_be_a_premise')
        if any(r['topic_id'] in {'ch7-paragraph37', 'ch9-paragraph27'} for r in f['source_refs']):
            require(not any(any(name in a.casefold() for name in ('ametist', 'sapfir', 'yoqut', 'rubin'))
                            for a in [f['claim'], *f['verified_answers']]),
                    'unresolved_gem_host_cannot_be_a_premise')
        if any(r['topic_id'] == 'ch9-paragraph27' for r in f['source_refs']):
            require(not any(('Al(OH)3' in a or 'Al(OH)₃' in a) and 'KOH' in a
                            for a in f['verified_answers']),
                    'unresolved_aluminium_koh_equation_cannot_be_an_answer')
        if any(r['topic_id'] in {'ch7-paragraph42', 'ch7-paragraph43', 'ch7-paragraph46', 'ch7-paragraph48'} for r in f['source_refs']):
            require(not any(re.search(r'(?<![A-Za-z])(?:HJ|KJ|NaJ|AgJ|J[2₂])(?![A-Za-z])', a)
                            for a in [f['claim'], *f['verified_answers']]),
                    'unresolved_legacy_iodine_notation_cannot_be_a_premise')
        if any(r['topic_id'] in {'ch7-paragraph42', 'ch7-paragraph43', 'ch7-paragraph50'} for r in f['source_refs']):
            held_acid = any(x in f['claim'] for x in ('H3PO3', 'H₃PO₃', 'H3BO3', 'H₃BO₃'))
            require(not held_acid or (not any('negiz' in a.casefold() or 'valent' in a.casefold()
                                            for a in [f['claim'], *f['verified_answers']])
                                      and not any(a in {'1', '2', '3'} for a in f['verified_answers'])),
                    'unresolved_acid_basicity_cannot_be_a_premise')
        if any(r['topic_id'] == 'ch7-paragraph48' for r in f['source_refs']):
            values = [a.translate(str.maketrans('₀₁₂₃₄₅₆₇₈₉', '0123456789')).replace(' ', '')
                      for a in [f['claim'], *f['verified_answers']]]
            require(not any('CuCl2' in a and 'NaOH' in a and
                            ('Cu(OH)2' in a or '=(OH)2' in a) for a in values),
                    'unresolved_missing_copper_equation_cannot_be_a_premise')
        if any(r['topic_id'] == 'ch7-paragraph50' for r in f['source_refs']):
            require(not any(re.search(r'(?<![0-9])32[.,]6[67](?![0-9])', a)
                            or ('oltingugurt' in a.casefold() and ('CO2' in a or 'CO₂' in a))
                            for a in [f['claim'], *f['verified_answers']]),
                    'unresolved_equivalent_gas_or_precision_cannot_be_a_premise')
    content = lesson.get("content", {})
    require(set(content) == {"cards", "formulas", "examples", "xp_reward", "source_refs"}
            and content["xp_reward"] == 20, "common_learning_content_required")
    require(type(content['formulas']) is list and type(content['examples']) is list,
            'reviewed_calculation_lists_required')
    source_refs(content["source_refs"])
    require(content["cards"] and lesson.get("assessments"), "teaching_and_assessments_required")
    taught = set()

    def fact_links(item):
        ids = item.get("fact_ids", [])
        require(ids and len(ids) == len(set(ids)) and set(ids) <= facts.keys(), "unknown_fact_reference")
        source_refs(item.get("source_refs"))
        needed = {fingerprint(r) for fid in ids for r in facts[fid]["source_refs"]}
        require(needed <= {fingerprint(r) for r in item["source_refs"]}, "missing_fact_citation")
        return set(ids)

    for card in content["cards"]:
        require(set(card) == {"title", "body", "source_refs", "fact_ids"}
                and type(card["title"]) is str and card["title"]
                and type(card["body"]) is str and card["body"], "original_card_required")
        taught |= fact_links(card)
    require(taught == facts.keys(), "untaught_fact_in_lesson")
    for item in content['formulas'] + content['examples']:
        require(set(item) == {'title', 'body', 'source_refs', 'fact_ids'}
                and type(item['title']) is str and item['title']
                and type(item['body']) is str and item['body'], 'reviewed_calculation_item_required')
        require(fact_links(item) <= taught, 'calculation_fact_not_taught')
    keys, prompts = set(), set()
    for q in lesson["assessments"]:
        require(q.get("key") and q["key"] not in keys, "duplicate_assessment_key")
        keys.add(q["key"])
        ids = fact_links(q)
        require(ids <= taught, "question_fact_not_taught")
        public, spec = q["public"], q["grading_spec"]
        if any(r['topic_id'] == 'ch7-paragraph24' for r in q['source_refs']):
            require(public.get('unit') not in {'kJ', 'kJ/mol'},
                    'unresolved_heat_sign_cannot_be_an_answer')
        if any(r['topic_id'] == 'ch7-7' for r in q['source_refs']):
            if q.get('response_kind') == 'numeric_value' and public.get('unit') in {'l', 'ml'}:
                from services.chemistry_grading import canonical_number
                require(canonical_number(spec['verified_answer']) not in {'22.4', '22400'},
                        'unresolved_water_vapour_state_cannot_be_an_answer')
        if any(r['topic_id'] == 'ch7-paragraph18' for r in q['source_refs']):
            # The book omits the layer-thickness interpretation and current
            # exposure context. Do not turn those unresolved data into keys.
            answer_text = spec.get('verified_answer', '')
            from services.chemistry_grading import canonical_number
            try:
                concentration = canonical_number(answer_text.replace('%', '').strip())
            except ValueError:
                concentration = None
            require(public.get('unit') != 'mm' and not any(
                token in answer_text for token in ('10^-5', '10⁻⁵', '0.00001', '0,00001')),
                'unresolved_ozone_context_cannot_be_an_answer')
            require(not ((public.get('unit') == '%' or '%' in answer_text)
                         and concentration == '0.00001'),
                    'unresolved_ozone_context_cannot_be_an_answer')
        require(type(public.get("prompt")) is str and public["prompt"]
                and public["prompt"].casefold() not in prompts, "unique_original_prompt_required")
        prompts.add(public["prompt"].casefold())
        require(spec.get("kind") == q["response_kind"], "assessment_kind_mismatch")
        if q['response_kind'] == 'numeric_value':
            require(spec['verified_answer'] in {a for fid in ids for a in facts[fid]['verified_answers']},
                    'unverified_numeric_answer_key')
        else:
            # Evidence labels may include printed numerical/symbol labels. This
            # comparison never grades learner text; the kind-specific grader does.
            def evidence_key(value):
                try:
                    return ('text', normalized_text(value))
                except ValueError:
                    return ('literal', value)
            verified = {evidence_key(a) for fid in ids for a in facts[fid]["verified_answers"]}
            require(evidence_key(spec["verified_answer"]) in verified, "unverified_answer_key")
        if q["response_kind"] == "concept_selection":
            require(set(public) == {"prompt", "options"}, "private_or_unknown_prompt_field")
            options = public["options"]
            require(len(options) == 4 and all(set(o) == {"id", "label"} for o in options)
                    and len({o["id"] for o in options}) == 4
                    # Chemical symbols are case-sensitive: H, h, Hg and HG
                    # are distinct displayed choices. IDs remain authoritative.
                    and len({o["label"].strip() for o in options}) == 4,
                    "four_unique_mcq_options_required")
            correct = [o for o in options if o["id"] == spec["expected"]]
            require(len(correct) == 1 and correct[0]["label"] == spec["verified_answer"], "mcq_answer_fact_mismatch")
            require(spec.get("choice_ids") == [o["id"] for o in options], "choice_allowlist_required")
            sample = {"choice_id": spec["expected"]}
        elif q["response_kind"] == "short_text":
            require(set(public) == {"prompt", "input_label", "max_length"}
                    and public["max_length"] == 80 and public["input_label"], "bounded_short_text_input_required")
            require(spec["expected"] == spec["verified_answer"] and spec.get("aliases")
                    and normalized_text(spec["expected"]) in {normalized_text(a) for a in spec["aliases"]},
                    "reviewed_text_aliases_required")
            sample = {"value": spec["expected"]}
        elif q['response_kind'] == 'numeric_value':
            require(set(public) == {'prompt', 'input_label', 'max_length', 'unit'}
                    and public['max_length'] == 80 and public['input_label']
                    and type(public['unit']) is str and public['unit'] == spec.get('unit'),
                    'explicit_numeric_unit_required')
            require(spec['expected'] == spec['verified_answer'], 'numeric_answer_evidence_mismatch')
            sample = {'value': spec['expected']}
        elif q['response_kind'] in {'chemical_formula', 'chemical_equation'}:
            from services.chemistry_notation import formula, equation
            require(set(public) == {'prompt', 'input_label', 'max_length'}
                    and public['max_length'] == 80 and public['input_label'],
                    'bounded_notation_input_required')
            require(spec['expected'] == spec['verified_answer'], 'notation_answer_evidence_mismatch')
            if q['response_kind'] == 'chemical_formula':
                _, composition = formula(spec['expected'])
                for alias in spec.get('aliases', []):
                    require(formula(alias)[1] == composition, 'formula_alias_composition_mismatch')
            else:
                _, atoms, _ = equation(spec['expected'])
                require(atoms[0] == atoms[1], 'unbalanced_reviewed_equation')
            sample = {'value': spec['expected']}
        else:
            raise ValueError("unreviewed_response_kind")
        require(grade_answer(spec, sample) == "correct", "deterministic_answer_key_failed")
        feedback_codes = {"correct", "incorrect", "invalid_answer", "answer_required"}
        if q['response_kind'] == 'chemical_equation':
            feedback_codes |= {'incorrect_species', 'atom_imbalance', 'incorrect_ratio'}
        require(set(spec.get("feedback", {})) == feedback_codes
                and all(type(s) is str and s for s in spec["feedback"].values()), "authored_feedback_required")
        require(spec.get("solution"), "source_linked_solution_required")
        for step in spec["solution"]:
            require(step.get("body") and fact_links(step) <= ids, "solution_fact_not_taught")
    return book, topic


def load_lessons(catalog=None):
    """Only explicit digest-pinned reviewed files; never glob JSON drafts."""
    catalog = catalog or load_catalog()
    index = read_json(DIRECTORY / "chemistry_lessons.json")
    require(index.get("schema_version") == 1 and index.get("subject") == "kimyo", "reviewed_index_required")
    lessons, keys, topics, integrated_reviews = [], set(), set(), set()
    for item in index["lessons"]:
        require(Path(item["file"]).name == item["file"] and
                Path(item["review_file"]).name == item["review_file"], "manifest_path_escape")
        path = DIRECTORY / item["file"]
        review = read_json(DIRECTORY / item["review_file"])
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        require(digest == item["sha256"] == review["lesson_sha256"]
                and review["lesson_file"] == item["file"]
                and review.get("original_authorship") is True, "changed_content_requires_new_review")
        lesson = read_json(path)
        validate_lesson(catalog, lesson, review)
        records = {r['id']: r for b in catalog['books'] for r in b['records']}
        require(all(identifier in integrated_reviews for identifier in lesson.get('source_context_ids', [])
                    if records[identifier]['kind'] == 'review'),
                'review_context_must_already_be_integrated')
        require(lesson["key"] not in keys and lesson["topic_id"] not in topics, "duplicate_indexed_lesson")
        keys.add(lesson["key"]); topics.add(lesson["topic_id"])
        integrated_reviews.update(lesson.get('source_activity_ids', []))
        lessons.append(lesson)
    return lessons
