"""Pure Chemistry evidence validation. No ORM, DB, network or LLM imports.

Keep Biology's validator and Physics's unfinished preview untouched. Catalogue
mapping is distinct from scientific claim review and executable lesson readiness.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from services.chemistry_errata import validate_fact_erratum, validate_question_erratum, validate_resolution

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
    'ch7-practical07': 'ch7-practical7-clinical-source-scope',
    'ch7-9': 'ch7-review6-product-loss-scope',
    'ch7-laboratory15': 'ch7-lab15-acid-condition-scope',
    'ch8-paragraph01': 'ch8-p01-mol-definition-scope',
    'ch8-paragraph02': 'ch8-p02-rounding-scope',
    'ch8-paragraph03': 'ch8-p03-classification-scope',
    'ch8-paragraph04': 'ch8-p04-oxygen-and-phase-scope',
    'ch8-paragraph05': 'ch8-p05-nitrogen-valence-review',
    'ch8-paragraph06': 'ch8-p06-group-rule-scope',
    'ch8-paragraph07': 'ch8-p07-mass-model-scope',
    'ch8-paragraph08': 'ch8-p08-isotope-average-scope',
    'ch8-paragraph09': 'ch8-p09-classical-electron-model-scope',
    'ch8-paragraph11': 'ch8-p11-ground-state-scope',
    'ch8-paragraph12': 'ch8-p12-filling-state-review',
    'ch8-paragraph13': 'ch8-p13-valence-and-isotope-scope',
    'ch8-chapter03': 'ch8-ch03-bonding-intro-scope',
    'ch8-paragraph14': 'ch8-p14-tabulated-scale-scope',
    'ch8-paragraph15': 'ch8-p15-bond-molecule-scope',
    'ch8-paragraph16': 'ch8-p16-ionic-pair-scope',
    'ch8-paragraph17': 'ch8-p17-lattice-property-scope',
    'ch8-paragraph18': 'ch8-p18-oxidation-model-scope',
    'ch8-paragraph19': 'ch8-p19-redox-role-scope',
    'ch8-paragraph20': 'ch8-p20-reaction-condition-scope',
    'ch8-paragraph21': 'ch8-p21-generalization-scope',
    'ch8-paragraph22': 'ch8-p22-halogen-condition-review',
    'ch8-paragraph23': 'ch8-p23-solubility-state-review',
    'ch8-paragraph24': 'ch8-p24-gas-aqueous-scope',
    'ch8-paragraph25': 'ch8-p25-gas-state-precision-review',
    'ch8-paragraph26': 'ch8-p26-equivalent-definition-review',
    'ch8-paragraph27': 'ch8-p27-chloride-oxychlorine-review',
    'ch8-paragraph28': 'ch8-p28-halogen-medical-condition-review',
    'ch8-practical01': 'ch8-practical1-evidence-stoichiometry-review',
    'ch8-paragraph29': 'ch8-p29-oxygen-orbital-sulfur-scope',
    'ch8-paragraph30': 'ch8-p30-sulfide-condition-scope',
    'ch8-paragraph31': 'ch8-p31-sulfur-oxide-condition-review',
    'ch8-paragraph32': 'ch8-p32-acid-sulfate-conflict-review',
    'ch8-paragraph33': 'ch8-p33-rate-model-review',
    'ch8-paragraph34': 'ch8-p34-equilibrium-rate-state-review',
    'ch8-paragraph35': 'ch8-p35-production-yield-scope',
    'ch8-practical02': 'ch8-practical2-heat-fraction-condition-review',
    'ch8-chapter06': 'ch8-ch06-prefix-configuration-review',
    'ch8-paragraph36': 'ch8-p36-nitrogen-condition-scope',
    'ch8-paragraph37': 'ch8-p37-ammonia-aqueous-yield-scope',
    'ch8-paragraph38': 'ch8-p38-nitrogen-oxide-valence-state-review',
    'ch8-paragraph39': 'ch8-p39-nitrate-condition-valence-review',
    'ch8-practical03': 'ch8-practical3-copy-formula-phase-review',
    'ch8-paragraph40': 'ch8-p40-phosphorus-reactivity-model-review',
    'ch8-paragraph41': 'ch8-p41-phosphate-structure-balance-review',
    'ch8-practical04': 'ch8-practical4-lime-unknown-evidence-review',
    'ch8-paragraph42': 'ch8-p42-nutrient-mixture-scope-review',
    'ch8-paragraph43': 'ch8-p43-reporting-basis-arithmetic-review',
    'ch8-paragraph44': 'ch8-p44-biogen-clinical-essentiality-review',
    'ch8-practical05': 'ch8-practical5-table-nitrate-unknown-review',
    'ch8-laboratory01': 'ch8-lab1-amphoteric-observation-scope',
    'ch8-laboratory02': 'ch8-lab2-crystal-phase-scope',
    'ch8-laboratory03': 'ch8-lab3-halide-starch-observation-scope',
    'ch8-laboratory04': 'ch8-lab4-soil-unknown-scope',
    'ch8-laboratory05': 'ch8-lab5-halogen-condition-scope',
    'ch8-laboratory06': 'ch8-lab6-solvent-layer-scope',
    'ch8-laboratory07': 'ch8-lab7-mineral-formula-unit-scope',
    'ch8-laboratory08': 'ch8-lab8-sulfate-model-scope',
    'ch8-laboratory09': 'ch8-lab9-ammonia-ratio-observation-scope',
    'ch8-laboratory10': 'ch8-lab10-fertilizer-unknown-scope',
    'ch9-paragraph01': 'ch9-p1-periodic-mass-trend-model-review',
    'ch9-paragraph02': 'ch9-p2-bond-charge-universals-review',
    'ch9-paragraph03': 'ch9-p3-electrolyte-water-acid-scope-review',
    'ch9-paragraph04': 'ch9-p4-dissociation-stage-school-scope-review',
    'ch9-paragraph05': 'ch9-p5-electrolyte-degree-constant-scope-review',
    'ch9-paragraph06': 'ch9-p6-ion-exchange-condition-review',
    'ch9-paragraph07': 'ch9-p7-hydrolysis-water-balance-review',
    'ch9-paragraph08': 'ch9-p8-carbon-configuration-allotrope-review',
    'ch9-paragraph09': 'ch9-p9-carbon-adsorption-heat-review',
    'ch9-paragraph10': 'ch9-p10-carbon-oxide-phase-safety-review',
    'ch9-paragraph11': 'ch9-p11-carbonate-charge-hydrate-rounding-review',
    'ch9-paragraph12': 'ch9-p12-silicon-density-source-scope-review',
    'ch9-paragraph13': 'ch9-p13-silicon-silicate-species-scope-review',
    'ch9-paragraph14': 'ch9-p14-silicate-cement-arithmetic-scope-review',
    'ch9-paragraph15': 'ch9-p15-metal-classification-density-scope-review',
    'ch9-paragraph16': 'ch9-p16-alloy-conditional-composition-review',
    'ch9-paragraph17': 'ch9-p17-metal-properties-conditions-review',
    'ch9-paragraph18': 'ch9-p18-corrosion-charge-inhibitor-review',
    'ch9-paragraph19': 'ch9-p19-electrolysis-charge-products-review',
    'ch9-paragraph20': 'ch9-p20-alkali-source-scope-review',
    'ch9-paragraph21': 'ch9-p21-alkali-compound-copy-scope-review',
    'ch9-paragraph22': 'ch9-p22-soda-hydride-cycle-scope-review',
    'ch9-paragraph23': 'ch9-p23-alkaline-earth-mineral-clinical-scope-review',
    'ch9-paragraph24': 'ch9-p24-hardness-phase-biological-arithmetic-review',
    'ch9-paragraph25': 'ch9-p25-aluminium-electrode-mineral-scope-review',
    'ch9-paragraph26': 'ch9-p26-aluminium-balance-hydrate-scope-review',
    'ch9-paragraph28': 'ch9-p28-copper-phase-conditional-scope-review',
    'ch9-paragraph29': 'ch9-p29-silver-gold-clinical-thickness-scope-review',
    'ch9-paragraph30': 'ch9-p30-zinc-mercury-balance-clinical-review',
    'ch9-paragraph31': 'ch9-p31-chromium-condition-table-review',
    'ch9-paragraph32': 'ch9-p32-chromium-compounds-coefficient-review',
    'ch9-paragraph33': 'ch9-p33-manganese-oxidation-copy-review',
    'ch9-paragraph34': 'ch9-p34-iron-diagram-rust-scope-review',
    'ch9-paragraph35': 'ch9-p35-iron-complex-clinical-scope-review',
    'ch9-paragraph36': 'ch9-p36-castiron-carbon-boundary-review',
    'ch9-paragraph37': 'ch9-p37-steel-worked-copy-review',
    'ch9-paragraph38': 'ch9-p38-materials-universal-claim-review',
    'ch9-paragraph39': 'ch9-p39-environment-exposure-taxonomy-review',
    'ch9-paragraph40': 'ch9-p40-periodicity-bounded-correction-review',
    'ch9-paragraph41': 'ch9-p41-technology-rate-model-review',
    'ch9-practical01': 'ch9-practical01-soil-observation-limits-review',
    'ch9-practical02': 'ch9-practical02-closed-set-carbonate-branches-review',
    'ch9-practical03': 'ch9-practical03-closed-metal-models-review',
    'ch9-laboratory01': 'ch9-laboratory01-carbonate-two-stage-model-review',
    'ch9-laboratory02': 'ch9-laboratory02-missing-mineral-measurements-review',
    'ch9-laboratory03': 'ch9-laboratory03-missing-glass-measurements-review',
    'ch9-laboratory04': 'ch9-laboratory04-missing-thermal-hardness-data-review',
    'ch9-laboratory05': 'ch9-lab5-missing-alloy-measurements-review',
    'ch9-laboratory06': 'ch9-lab6-bounded-salt-displacement-review',
    'ch9-laboratory07': 'ch9-lab7-anode-starch-evidence-review',
    'ch9-laboratory08': 'ch9-lab8-aluminium-gas-coefficient-review',
    'ch9-laboratory09': 'ch9-lab9-missing-aluminium-strength-data-review',
    'ch9-laboratory10': 'ch9-lab10-hydroxide-drop-stoichiometry-review',
    'ch9-laboratory11': 'ch9-lab11-hydrolysis-speciation-scope-review',
    'ch9-laboratory12': 'ch9-lab12-copper-theoretical-volume-review',
    'ch9-laboratory13': 'ch9-lab13-zinc-missing-density-review',
    'ch9-laboratory14': 'ch9-lab14-chromium-condition-model-review',
    'ch9-laboratory15': 'ch9-lab15-iron-hydroxide-color-scope-review',
    'ch9-laboratory16': 'ch9-lab16-iron-complex-phase-formula-review',
    'ch9-laboratory17': 'ch9-lab17-alloy-rate-versus-amount-review',
    'ch10-paragraph01': 'ch10-p1-organic-generalizations-history-review',
    'ch10-paragraph02': 'ch10-p2-structure-caption-oxidation-review',
    'ch10-paragraph03': 'ch10-p3-isomer-figure-scope-review',
    'ch10-paragraph04': 'ch10-p4-classification-polymerization-review',
    'ch10-paragraph05': 'ch10-p5-rational-center-percentage-review',
    'ch10-paragraph06': 'ch10-p6-nomenclature-tie-rules-review',
    'ch10-paragraph07': 'ch10-p7-wurtz-name-phase-scope-review',
    'ch10-paragraph08': 'ch10-p8-cracking-caption-selectivity-review',
    'ch10-paragraph09': 'ch10-p9-ring-schematic-identity-review',
    'ch10-paragraph10': 'ch10-p10-combustion-data-ring-conditions-review',
    'ch10-paragraph11': 'ch10-p11-alkene-figure-mass-unit-review',
    'ch10-paragraph12': 'ch10-p12-ez-priority-route-scope-review',
    'ch10-paragraph13': 'ch10-p13-alkene-phase-selectivity-polymer-review',
    'ch10-paragraph14': 'ch10-p14-diene-bond-header-products-review',
    'ch10-paragraph15': 'ch10-p15-alkyne-identity-incomplete-chains-review',
    'ch10-paragraph16': 'ch10-p16-arene-selectivity-phase-routes-review',
    'ch10-paragraph17': 'ch10-p17-hybrid-angle-local-model-review',
    'ch10-paragraph18': 'ch10-p18-petroleum-fractions-caption-review',
    'ch10-paragraph19': 'ch10-p19-gas-coal-division-data-review',
    'ch10-paragraph20': 'ch10-p20-alcohol-definition-name-routes-review',
    'ch10-paragraph21': 'ch10-p21-alcohol-phase-threshold-chains-review',
    'ch10-paragraph22': 'ch10-p22-polyol-gemdiol-complex-scope-review',
    'ch10-paragraph23': 'ch10-p23-phenol-caption-complex-identity-review',
    'ch10-paragraph24': 'ch10-p24-aldehyde-name-speciation-model-review',
    'ch10-paragraph25': 'ch10-p25-ketone-graph-family-quantity-review',
    'ch10-paragraph26': 'ch10-p26-acid-name-coefficient-classification-review',
    'ch10-paragraph27': 'ch10-p27-ether-isomer-hybrid-count-review',
    'ch10-paragraph28': 'ch10-p28-ester-medium-identity-scope-review',
    'ch10-paragraph29': 'ch10-p29-fat-composition-phase-hydrolysis-review',
    'ch10-paragraph30': 'ch10-p30-carbohydrate-units-redox-scope-review',
    'ch10-paragraph31': 'ch10-p31-polysaccharide-endgroups-amount-units-review',
    'ch10-paragraph32': 'ch10-p32-nitro-carbon-classification-route-scope-review',
    'ch10-paragraph33': 'ch10-p33-amine-phase-basicity-isomer-scope-review',
    'ch10-paragraph34': 'ch10-p34-aminoacid-valence-peptide-color-model-review',
    'ch10-paragraph35': 'ch10-p35-polymer-endgroups-properties-rubber-rank-review',
    'ch10-laboratory01': 'ch10-lab1-ethanol-digital-cycle-safety-review',
    'ch10-laboratory02': 'ch10-lab2-acetylene-digital-observation-safety-review',
    'ch10-laboratory03': 'ch10-lab3-glycerol-complex-observation-scope-review',
    'ch10-laboratory04': 'ch10-lab4-acid-kinetics-indicator-digital-scope-review',
    'ch10-laboratory05': 'ch10-lab5-glucose-iodine-reagent-balance-scope-review',
    'ch10-laboratory06': 'ch10-lab6-protein-biuret-observation-scope-review',
    'ch11-paragraph01': 'ch11-p1-quantum-capacity-configuration-model-scope-review',
    'ch11-paragraph02': 'ch11-p2-periodic-shorttable-trend-configuration-scope-review',
    'ch11-paragraph03': 'ch11-p3-isotope-nuclear-charge-particle-count-scope-review',
    'ch11-paragraph04': 'ch11-p4-bond-polarity-lattice-localgraph-scope-review',
    'ch11-paragraph05': 'ch11-p5-mole-unit-mass-singleatom-scope-review',
    'ch11-paragraph06': 'ch11-p6-gas-volume-density-rounding-model-scope-review',
    'ch11-paragraph07': 'ch11-p7-equivalent-reaction-context-unit-scope-review',
    'ch11-paragraph08': 'ch11-p8-ideal-gas-unit-temperature-identity-scope-review',
    'ch11-paragraph09': 'ch11-p9-electrolyte-solubility-lamp-scope-review',
    'ch11-paragraph10': 'ch11-p10-dissociation-degree-ionic-count-model-scope-review',
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
            if r['id'] in KNOWN_SOURCE_HOLDS:
                hold = r.get('source_review_hold', {})
                require(hold.get('id') == KNOWN_SOURCE_HOLDS[r['id']],
                        'known_source_conflict_must_remain_on_review_hold')
                if hold.get('status') == 'open':
                    require(r.get('fact_review_status') == 'blocked_source_conflict'
                            and not r.get('reviewed_erratum_ids'),
                            'known_source_conflict_must_remain_on_review_hold')
                else:
                    validate_resolution(catalog, r)
            else:
                require(not r.get('reviewed_erratum_ids'), 'unsupported_source_erratum')
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


def source_is_blocked(catalog, record):
    if record.get('id') in KNOWN_SOURCE_HOLDS:
        if record.get('source_review_hold', {}).get('status') == 'open':
            return True
        validate_resolution(catalog, record)
        return False
    return record.get('source_review_hold', {}).get('status') == 'open'


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


def _validate_indexed_context(catalog, identifier):
    """Standalone validation also requires an immutable reviewed earlier lesson.

    load_lessons supplies its already-validated prefix, avoiding repeated reads.
    Earlier-grade links strictly decrease grade, so recursive review terminates.
    """
    index = read_json(DIRECTORY / 'chemistry_lessons.json')
    for item in index['lessons']:
        require(Path(item['file']).name == item['file'] and
                Path(item['review_file']).name == item['review_file'], 'manifest_path_escape')
        path = DIRECTORY / item['file']
        context = read_json(path)
        if context.get('topic_id') != identifier:
            continue
        evidence = read_json(DIRECTORY / item['review_file'])
        require(hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256']
                == evidence['lesson_sha256'] and evidence['lesson_file'] == item['file']
                and evidence.get('original_authorship') is True,
                'changed_context_requires_new_review')
        validate_lesson(catalog, context, evidence)
        return
    raise ValueError('earlier_grade_context_must_be_reviewed_and_indexed')


def validate_lesson(catalog, lesson, review, *, reviewed_context_topics=None):
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
    require(not source_is_blocked(catalog, topic),
            'unresolved_source_review_issue')
    require(lesson.get("sequence") == topic["sequence"] and
            lesson.get("prerequisite_ids") == topic["prerequisite_ids"], "lesson_order_mismatch")
    require(type(lesson.get("revision")) is int and lesson["revision"] > 0,
            "positive_reviewed_revision_required")
    records = {r['id']: r for b in catalog['books'] for r in b['records']}
    source_books = {r['id']: b for b in catalog['books'] for r in b['records']}
    allowed_sources = {topic['id']: topic}
    chapter_prefix_limits = {}
    for field in ('source_context_ids', 'source_activity_ids'):
        linked = lesson.get(field, [])
        require(type(linked) is list and all(type(x) is str for x in linked)
                and len(linked) == len(set(linked)),
                'explicit_unique_source_links_required')
        for identifier in linked:
            record = records.get(identifier)
            require(record and identifier not in allowed_sources
                    and not source_is_blocked(catalog, record),
                    'unknown_or_blocked_linked_source')
            context_book = source_books[identifier]
            if context_book['id'] != book['id']:
                require(field == 'source_context_ids' and record['kind'] in TEACHING_KINDS,
                        'earlier_grade_teaching_context_only')
                require(context_book['grade'] < book['grade'],
                        'source_context_grade_must_precede_lesson')
                if reviewed_context_topics is None:
                    _validate_indexed_context(catalog, identifier)
                else:
                    require(identifier in reviewed_context_topics,
                            'earlier_grade_context_must_already_be_validated')
                allowed_sources[identifier] = record
                continue
            if field == 'source_context_ids':
                if record['kind'] == 'chapter':
                    first = min((r for r in book['records'] if r['kind'] in TEACHING_KINDS
                                 and r['chapter_id'] == record['id']), key=lambda r: r['sequence'])
                    require(record['id'] == topic['chapter_id']
                            and record['printed_start'] < first['printed_start']
                            and first['sequence'] <= topic['sequence'],
                            'source_chapter_prefix_must_precede_lesson')
                    chapter_prefix_limits[identifier] = first['printed_start']
                elif record['kind'] == 'review':
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
            cited_book = source_books.get(ref.get('topic_id'))
            require(evidence and evidence.get("verification") == "page_image_reviewed"
                    and ref.get("verification") == "page_image_reviewed"
                    and re.fullmatch(r"[0-9a-f]{64}", evidence.get("page_image_sha256", "")),
                    "original_page_image_review_required")
            require(cited_book and ref.get("book_id") == cited_book["id"] == evidence["book_id"]
                    and ref.get("sha256") == cited_book["sha256"] == evidence["sha256"]
                    and ref.get("file_name") == cited_book["file_name"]
                    and cited and ref.get("topic_id") == cited["id"] == evidence["topic_id"]
                    and ref.get("paragraph") == (None if cited['kind'] == 'chapter' else cited["number"]), "claim_source_identity_mismatch")
            require(ref.get('book_title') == cited_book['title'] and ref.get('authors') == cited_book['authors']
                    and ref.get('year') == cited_book['year'] and ref.get('topic_title') == cited['title'],
                    'claim_bibliography_mismatch')
            pp = ref.get("printed_pages", [])
            require(pp == [evidence["printed_page"]] and
                    cited["printed_start"] <= pp[0] <= cited["printed_end"], "claim_outside_topic")
            if cited['kind'] == 'chapter':
                limit = chapter_prefix_limits[cited['id']]
                require(pp[0] < limit or (pp[0] == limit
                        and ref.get('page_scope') == evidence.get('page_scope')
                        == 'before_first_teaching_heading'), 'claim_outside_chapter_prefix')
            loc = page_locator(cited_book["grade"], pp[0])
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
        validate_fact_erratum(catalog, f, pages)
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
        if any(r['topic_id'] == 'ch7-practical07' for r in f['source_refs']):
            require(not any('regidron' in a.casefold() or 'регидрон' in a.casefold()
                            for a in [f['claim'], *f['verified_answers']]),
                    'held_clinical_recipe_cannot_be_a_premise')
        if any(r['topic_id'] == 'ch7-laboratory15' for r in f['source_refs']):
            require(not any('H2SO4' in (plain := a.translate(str.maketrans('₀₁₂₃₄₅₆₇₈₉', '0123456789')).replace(' ', ''))
                            and re.search(r'(?<![A-Za-z])(?:[0-9]+)?Cu(?=[+=→]|$)', plain)
                            and ('=' in plain or '→' in plain)
                            for a in [f['claim'], *f['verified_answers']]),
                    'unresolved_lab_copper_acid_conditions_cannot_be_a_premise')
        topic_ids = {r['topic_id'] for r in f['source_refs']}
        plain_values = [a.translate(str.maketrans('₀₁₂₃₄₅₆₇₈₉', '0123456789'))
                        for a in [f['claim'], *f['verified_answers']]]
        if 'ch8-paragraph01' in topic_ids:
            require(not any(re.search(r'1\s*mol\s*=\s*(?:[0-9.,]+\s*)?(?:g\b|gram)', a, re.I)
                            for a in plain_values), 'unresolved_mol_mass_identity_cannot_be_a_premise')
        if 'ch8-paragraph02' in topic_ids:
            require(not any(re.search(r'(?<![0-9])(?:34[.,]6[12]|43[.,]2[45])(?![0-9])', a)
                            for a in f['verified_answers']), 'unresolved_grade8_rounding_cannot_be_an_answer')
        if 'ch8-paragraph04' in topic_ids:
            require(not any('O2' in a and ('Na2O2' in a or 'K2O2' in a)
                            and ('=' in a or '→' in a) for a in plain_values),
                    'unresolved_alkali_oxygen_equation_cannot_be_a_premise')
        if 'ch8-paragraph05' in topic_ids:
            require(not any('N2O5' in a and ('valent' in a.casefold() or 'IV' in a or 'V' in a)
                            for a in plain_values), 'unresolved_nitrogen_valence_cell_cannot_be_a_premise')
        if 'ch8-paragraph06' in topic_ids:
            require(not ('geliy' in f['claim'].casefold() and 'tashqi' in f['claim'].casefold()
                         and '8' in f['verified_answers']),
                    'unresolved_helium_group_rule_cannot_be_an_answer')
        if 'ch8-paragraph07' in topic_ids:
            require(not any(re.search(r'A_?r\s*=\s*N\s*\+\s*Z', a) for a in plain_values),
                    'unresolved_average_mass_identity_cannot_be_a_premise')
        if 'ch8-paragraph08' in topic_ids:
            require(not any(re.search(r'(?<![0-9])35[.,](?:543|4846)(?![0-9])', a)
                            for a in f['verified_answers']), 'unresolved_isotope_chart_average_cannot_be_an_answer')
            require(not any('tabiiy kaliy' in a.casefold() and re.search(r'(?<![0-9])(?:7|93)\s*%', a)
                            for a in plain_values), 'unresolved_natural_potassium_abundance_cannot_be_a_premise')
        if 'ch8-paragraph09' in topic_ids:
            require(not any('markazdan qochma' in a.casefold() for a in plain_values),
                    'unresolved_classical_electron_force_cannot_be_a_premise')
        if 'ch8-paragraph12' in topic_ids:
            require(not any(re.search(r'(?<![A-Za-z])(?:La|Ce)(?![a-z])', a)
                            for a in [f['claim'], *f['verified_answers']]),
                    'unresolved_la_ce_configuration_cannot_be_a_premise')
        if 'ch8-paragraph13' in topic_ids:
            require(not any(re.search(r'(?<![0-9])35[.,](?:543|4846)(?![0-9])', a)
                            for a in f['verified_answers']), 'unresolved_natural_chlorine_average_cannot_be_an_answer')
            require(not ('geliy' in f['claim'].casefold() and any(a.casefold() == 'metall'
                            for a in f['verified_answers'])), 'unresolved_two_electrons_metal_rule_cannot_be_a_premise')
        if 'ch8-paragraph15' in topic_ids:
            require(not any(('CH4' in a or 'CH₄' in a) and 'molekula' in a.casefold()
                            and 'qutbli' in a.casefold() for a in [f['claim'], *f['verified_answers']]),
                    'unreviewed_molecule_geometry_cannot_be_a_premise')
        if topic_ids & {'ch8-paragraph18', 'ch8-paragraph19'}:
            require(not any('kislorod' in a.casefold() and 'doimo' in a.casefold()
                            and re.search(r'[−-]2', a) for a in plain_values),
                    'unresolved_universal_oxygen_state_cannot_be_a_premise')
        if 'ch8-paragraph19' in topic_ids:
            require(not any('barcha metall ionlari' in a.casefold() and 'qaytaruvchi' in a.casefold()
                            for a in plain_values), 'unresolved_universal_metal_ion_role_cannot_be_a_premise')
        if 'ch8-paragraph20' in topic_ids:
            require(not any('N2O' in a and 'har bir' in a.casefold() and '+1' in a
                            for a in plain_values), 'unreviewed_individual_nitrogen_site_cannot_be_a_premise')
        if 'ch8-paragraph21' in topic_ids:
            require(not any('barcha inert gaz' in a.casefold() and 'RO4' in a
                            for a in plain_values), 'unreviewed_universal_noble_oxide_cannot_be_a_premise')
        if 'ch8-paragraph22' in topic_ids:
            require(not any(re.search(r'(?<![0-9])1866(?![0-9])', a)
                            for a in f['verified_answers']), 'unresolved_halogen_history_date_cannot_be_an_answer')
        if 'ch8-paragraph23' in topic_ids:
            require(not any(re.search(r'(?<![0-9])0[.,]63(?![0-9])', a)
                            for a in f['verified_answers']), 'unresolved_chlorine_solubility_state_cannot_be_an_answer')
        if 'ch8-paragraph24' in topic_ids:
            require(not any(a.strip() == '500' for a in f['verified_answers']),
                    'unresolved_hcl_solubility_conditions_cannot_be_an_answer')
        if 'ch8-paragraph25' in topic_ids:
            require(not any(re.search(r'(?<![0-9])112(?![0-9])', a)
                            for a in f['verified_answers']), 'unresolved_water_vapour_state_cannot_be_an_answer')
        if 'ch8-paragraph26' in topic_ids:
            require(not any(a.strip() == '9' for a in f['verified_answers']),
                    'unresolved_equivalent_target_mismatch_cannot_be_an_answer')
        if 'ch8-paragraph27' in topic_ids:
            require(not any('HgCl2' in a and 'erimaydi' in a.casefold()
                            for a in plain_values), 'unreviewed_mercury_chloride_solubility_cannot_be_a_premise')
        if 'ch8-paragraph28' in topic_ids:
            require(not any('uyqusizlik' in a.casefold() for a in plain_values),
                    'unverified_halogen_clinical_treatment_cannot_be_a_premise')
        if 'ch8-practical01' in topic_ids:
            require(not any('Ca(OH)2' in a.replace(' ', '') and '2CaCl2' in a.replace(' ', '')
                            and ('=' in a or '→' in a) for a in plain_values),
                    'unbalanced_calcium_hydroxide_copy_cannot_be_a_premise')
            require(not any(re.search(r'2[.,]45\s*[·*×]\s*0[.,]75\s*=\s*3[.,]27', a)
                            for a in plain_values), 'incorrect_solution_fraction_operation_cannot_be_a_premise')
        if 'ch8-paragraph29' in topic_ids:
            require(not ('Se' in f['claim'] and '79' in f['verified_answers']),
                    'unreviewed_selenium_isotope_label_cannot_be_an_answer')
        if 'ch8-paragraph30' in topic_ids:
            require(not any('H2S' in a and 'xavfsiz' in a.casefold() for a in plain_values),
                    'unverified_sulfide_exposure_threshold_cannot_be_a_premise')
        if 'ch8-paragraph31' in topic_ids:
            require(not any(re.search(r'(?<![0-9])0[.,]0[35](?![0-9])', a)
                            for a in f['verified_answers']), 'unverified_sulfur_oxide_exposure_limit_cannot_be_an_answer')
        if 'ch8-paragraph32' in topic_ids:
            require(not any('CaSO4' in a and re.search(r'(?:1/4|¼|0[.,]25)\s*H2O', a)
                            for a in plain_values), 'unresolved_gypsum_hydrate_quantity_cannot_be_a_premise')
            require(not any(re.search(r'(?<![A-Za-z])Ag(?![a-z])', a)
                            and ('etmaydi' in a.casefold() or 'kirishmaydi' in a.casefold())
                            for a in plain_values), 'unresolved_silver_acid_nonreaction_cannot_be_a_premise')
        if 'ch8-paragraph33' in topic_ids:
            require(not any('barcha reaksiyalarda' in a.casefold() and 'koeffitsiyent' in a.casefold()
                            and 'tartib' in a.casefold() for a in plain_values),
                    'unreviewed_universal_reaction_order_cannot_be_a_premise')
        if 'ch8-paragraph34' in topic_ids:
            require(not any('harorat pasaysa' in a.casefold() and 'tezlashadi' in a.casefold()
                            for a in plain_values), 'unresolved_equilibrium_shift_rate_confusion_cannot_be_a_premise')
        if 'ch8-paragraph35' in topic_ids:
            require(not any(re.search(r'(?<![0-9])(?:99[.,]2|73)(?![0-9])', a)
                            for a in f['verified_answers']), 'unqualified_production_yield_cannot_be_an_answer')
        if 'ch8-practical02' in topic_ids:
            require(not any('O3' in a and ('Q' in a or '192' in a) for a in plain_values),
                    'unresolved_ozone_formation_heat_cannot_be_a_premise')
            if any(r['printed_pages']==[154] for r in f['source_refs']) and 'massa ulushi' in f['claim'].casefold():
                require(not any(re.search(r'(?<![0-9])(?:2[.,]45|4[.,]9)(?![0-9])', a)
                                for a in f['verified_answers']), 'unresolved_solution_total_mass_cannot_be_an_answer')
        if 'ch8-chapter06' in topic_ids:
            require(not any('5p10' in a.replace(' ', '') for a in plain_values),
                    'unresolved_bismuth_p_capacity_copy_cannot_be_a_premise')
        if 'ch8-paragraph36' in topic_ids:
            require(not any('barcha metallar' in a.casefold() and 'kirishmaydi' in a.casefold()
                            for a in plain_values), 'unqualified_nitrogen_metal_nonreaction_cannot_be_a_premise')
        if 'ch8-paragraph37' in topic_ids:
            require(not any('harorat pasaysa' in a.casefold() and 'unum kamayadi' in a.casefold()
                            for a in plain_values), 'unresolved_ammonia_yield_rate_confusion_cannot_be_a_premise')
        if 'ch8-paragraph38' in topic_ids:
            require(not any('N2O5' in a and 'valent' in a.casefold() for a in plain_values),
                    'unresolved_nitrogen_pentoxide_valence_cannot_be_a_premise')
        if 'ch8-practical03' in topic_ids:
            require(not any('Ca(CN)2' in a.replace(' ', '') for a in plain_values),
                    'unresolved_cyanamide_formula_identity_cannot_be_a_premise')
            require(not any('NH3+NH3' in a.replace(' ', '') for a in plain_values),
                    'unresolved_ammonia_reagent_copy_cannot_be_a_premise')
        if 'ch8-paragraph40' in topic_ids:
            require(not any('2P+3H2=2PH3' in a.replace(' ', '') for a in plain_values),
                    'unreviewed_direct_phosphine_formation_cannot_be_a_premise')
            require(not any('qizil fosfor zaharsiz' in a.casefold() for a in plain_values),
                    'unqualified_phosphorus_safety_claim_cannot_be_a_premise')
        if 'ch8-paragraph41' in topic_ids:
            require(not any(re.search(r'P2O5\+6KOH=2K3PO4\+H2O(?![0-9])', a.replace(' ', ''))
                            for a in plain_values), 'unbalanced_phosphate_water_copy_cannot_be_a_premise')
            require(not any('barcha fosfatlar erimaydi' in a.casefold() for a in plain_values),
                    'unqualified_phosphate_solubility_cannot_be_a_premise')
        if 'ch8-paragraph43' in topic_ids:
            require(not any(re.search(r'(?<![0-9])(?:16[.,]4|4[.,]117|473[.,]3)(?![0-9])', a)
                            for a in f['verified_answers']), 'unresolved_fertilizer_arithmetic_cannot_be_an_answer')
        if 'ch8-paragraph44' in topic_ids:
            require(not any('askaltsiy' in a.casefold() or 'askalsiy' in a.casefold()
                            or 'c vitamini' in a.casefold() for a in plain_values),
                    'unreviewed_biogen_clinical_claim_cannot_be_a_premise')
            require(not any('barcha mikroelementlar' in a.casefold() and 'zarur' in a.casefold()
                            for a in plain_values), 'unqualified_trace_element_essentiality_cannot_be_a_premise')
        if 'ch8-laboratory01' in topic_ids:
            require(not any('barcha gidroksidlar' in a.casefold() and 'ishqorda eriydi' in a.casefold()
                            for a in plain_values), 'unqualified_hydroxide_alkali_dissolution_cannot_be_a_premise')
        if 'ch8-laboratory03' in topic_ids:
            require(not any('kraxmal' in a.casefold() and ('ko‘k' in a.casefold() or "ko'k" in a.casefold())
                            for a in plain_values), 'unprovided_starch_color_cannot_be_a_premise')
        if 'ch8-laboratory04' in topic_ids:
            require(not any('barcha tuproq' in a.casefold() and 'xlorid' in a.casefold()
                            for a in plain_values), 'unprovided_soil_chloride_result_cannot_be_a_premise')
        if 'ch8-laboratory06' in topic_ids:
            require(not any('benzol' in a.casefold() and ('qatlam binafsha' in a.casefold() or 'qatlami binafsha' in a.casefold())
                            for a in plain_values), 'unprovided_iodine_layer_color_cannot_be_a_premise')
        if 'ch8-laboratory09' in topic_ids:
            require(not any('1.5:1' in a.replace(',', '.') and 'stexiometrik' in a.casefold()
                            for a in f['verified_answers']), 'recipe_is_not_exact_stoichiometric_mass_answer')
        if 'ch9-paragraph01' in topic_ids:
            require(not any('0.269' in a.replace(',', '.') and 'mg' in a.casefold()
                            for a in plain_values), 'unreviewed_magnesium_radius_cannot_be_a_premise')
            require(not any('barcha davrlarda' in a.casefold() and 'ionlanish' in a.casefold()
                            and 'qat’iy ortadi' in a.casefold() for a in plain_values),
                    'unqualified_monotonic_ionization_cannot_be_a_premise')
            require(not any('Ar-Z' in a.replace(' ', '').replace('−', '-')
                            for a in f['verified_answers']),
                    'average_atomic_mass_neutron_rule_cannot_be_an_answer')
        if 'ch9-paragraph03' in topic_ids:
            require(not any('H3PO3' in a and ('3H+' in a.replace(' ', '') or 'uchta kislotali' in a.casefold())
                            for a in plain_values), 'unverified_phosphorous_acid_three_protons_cannot_be_a_premise')
        if 'ch9-paragraph05' in topic_ids:
            require(not any('barcha organik' in a.casefold() and 'kuchsiz' in a.casefold()
                            for a in plain_values), 'unqualified_all_organic_weak_cannot_be_a_premise')
            require('58' not in f['verified_answers'],
                    'ambiguous_sulfate_dissociation_degree_cannot_be_an_answer')
        if 'ch9-paragraph06' in topic_ids:
            require(not any('H2S suvda erimaydi' in a for a in plain_values),
                    'unqualified_hydrogen_sulfide_insolubility_cannot_be_a_premise')
        if 'ch9-paragraph07' in topic_ids:
            require(not any('kuchsiz asos va kuchsiz kislota' in a.casefold() and
                            'barcha' in a.casefold() and 'to‘liq' in a.casefold() for a in plain_values),
                    'unqualified_complete_weak_salt_hydrolysis_cannot_be_a_premise')
            require(not any(re.search(r'Fe\(OH\)2(?![A-Za-z0-9])', a) and 'FeCl3' in a for a in plain_values),
                    'unreviewed_ferric_carbonate_hydroxide_copy_cannot_be_a_premise')
        if 'ch9-paragraph08' in topic_ids:
            require(not any(a.replace(' ', '') in {'1s22s22p6', '2p6'} for a in f['verified_answers']),
                    'unreviewed_carbon_configuration_copy_cannot_be_an_answer')
            require(not any('fulleren' in a.casefold() and '80' in a for a in plain_values),
                    'unreviewed_fullerene_atom_count_cannot_be_a_premise')
        if 'ch9-paragraph09' in topic_ids:
            require(not any('qonni tozalash' in a.casefold() for a in plain_values),
                    'unreviewed_adsorption_clinical_claim_cannot_be_a_premise')
        if 'ch9-paragraph10' in topic_ids:
            require(not any('CO2' in a and 'barcha yong‘in' in a.casefold() for a in plain_values),
                    'unqualified_carbon_dioxide_fire_safety_cannot_be_a_premise')
        if 'ch9-paragraph11' in topic_ids:
            require(not any(any(bad in a for bad in ('HCO3²−', 'HCO3²⁻', 'HCO3(2-)')) for a in plain_values),
                    'unbalanced_bicarbonate_charge_copy_cannot_be_a_premise')
            require(not any(a.replace(',', '.') in {'2.74', '20.4'} for a in f['verified_answers']),
                    'unresolved_carbonate_arithmetic_or_volume_copy_cannot_be_an_answer')
        if 'ch9-paragraph12' in topic_ids:
            require(not any(a.replace(',', '.') in {'3.3', '2.33'} for a in f['verified_answers']),
                    'unreviewed_silicon_phase_density_cannot_be_an_answer')
        if 'ch9-paragraph13' in topic_ids:
            require(not any('barcha silan' in a.casefold() and 'n<8' in a.replace(' ', '') for a in plain_values),
                    'unqualified_silane_chain_limit_cannot_be_a_premise')
        if 'ch9-paragraph14' in topic_ids:
            require(not any('450' in a and ('sement' in a.casefold() or 'klinker' in a.casefold()) for a in plain_values),
                    'unreviewed_cement_temperature_cannot_be_a_premise')
            require(not any(a.replace(',', '.')=='0.953' for a in f['verified_answers']),
                    'unresolved_limestone_fraction_rounding_cannot_be_an_answer')
        if 'ch9-paragraph15' in topic_ids:
            require(not any('500' in a and 'chegara' in a.casefold() and 'kg/m3' in a for a in plain_values),
                    'unreviewed_metal_density_threshold_cannot_be_a_premise')
        if 'ch9-paragraph16' in topic_ids:
            require(not any('barcha qotishma' in a.casefold() and 'yuqori' in a.casefold() for a in plain_values),
                    'unqualified_alloy_conductivity_cannot_be_a_premise')
        if 'ch9-paragraph17' in topic_ids:
            require(not any('har bir metall' in a.casefold() and 'barcha' in a.casefold()
                            and 'siqib' in a.casefold() for a in plain_values),
                    'unqualified_aqueous_displacement_cannot_be_a_premise')
        if 'ch9-paragraph18' in topic_ids:
            require(not any('10^6' in a and 'mol/L' in a for a in plain_values),
                    'unreviewed_inhibitor_concentration_cannot_be_a_premise')
            require(not any('barcha zang' in a.casefold() and 'Fe(OH)3' in a for a in plain_values),
                    'unqualified_rust_identity_cannot_be_a_premise')
        if 'ch9-paragraph19' in topic_ids:
            require(not any('H2S' in a and 'anod' in a.casefold() and 'barcha' in a.casefold() for a in plain_values),
                    'unreviewed_sulfide_anode_product_cannot_be_a_premise')
            require(not any('2H++2e=H+' in a.replace(' ', '') for a in plain_values),
                    'unbalanced_electrolysis_hydrogen_copy_cannot_be_a_premise')
        if 'ch9-paragraph20' in topic_ids:
            require(not any('fransiy' in a.casefold() and 'tabiatda uchramaydi' in a.casefold() for a in plain_values),
                    'unreviewed_francium_occurrence_cannot_be_a_premise')
            require(not any('seziy' in a.casefold() and 'zaharli emas' in a.casefold() for a in plain_values),
                    'unqualified_alkali_toxicity_cannot_be_a_premise')
        if 'ch9-paragraph21' in topic_ids:
            require(not any(a.strip() == 'NaON' for a in f['verified_answers']),
                    'unreviewed_sodium_hydroxide_label_cannot_be_an_answer')
            require(not any('KO2' in a and 'peroksid' in a.casefold() for a in f['verified_answers']),
                    'unreviewed_potassium_oxygen_category_cannot_be_an_answer')
        if 'ch9-paragraph22' in topic_ids:
            require(not any('har qanday' in a.casefold() and 'gidrid' in a.casefold() and 'KH' in a for a in plain_values),
                    'unqualified_hydride_identity_cannot_be_a_premise')
        if 'ch9-paragraph23' in topic_ids:
            require(not any('MgSiO3' in a and 'olivin' in a.casefold() for a in plain_values),
                    'unreviewed_olivine_formula_cannot_be_a_premise')
            require(not any('askalsiy' in a.casefold() and 'davola' in a.casefold() for a in plain_values),
                    'unreviewed_alkaline_earth_clinical_claim_cannot_be_a_premise')
        if 'ch9-paragraph24' in topic_ids:
            require(not any(a.replace(',', '.') == '165' for a in f['verified_answers']),
                    'unresolved_milk_arithmetic_copy_cannot_be_an_answer')
        if 'ch9-paragraph25' in topic_ids:
            require(not any('katod musbat' in a.casefold() for a in plain_values),
                    'unreviewed_aluminium_electrode_sign_cannot_be_a_premise')
            require(not any(a.replace(' ', '') == 'O2+2C=CO' for a in f['verified_answers']),
                    'unbalanced_aluminium_carbon_copy_cannot_be_an_answer')
        if 'ch9-paragraph26' in topic_ids:
            require(not any(a.replace(' ', '') == '2Al+2NaOH+6H2O=2Na[Al(OH)4]+H2' for a in f['verified_answers']),
                    'unbalanced_aluminium_hydrogen_copy_cannot_be_an_answer')
        if 'ch9-paragraph27' in topic_ids:
            require(not any(a.replace(' ', '') == 'Al(OH)3+2KOH=KAlO2+2H2O' for a in f['verified_answers']),
                    'unbalanced_aluminium_potassium_copy_cannot_be_an_answer')
            require(not any('korund' in a.casefold() and 'ametist' in a.casefold() for a in plain_values),
                    'unreviewed_corundum_amethyst_identity_cannot_be_a_premise')
        if 'ch9-paragraph28' in topic_ids:
            require(not any('Cu hech qachon oksidlanmaydi'.casefold() in a.casefold() for a in plain_values),
                    'unqualified_copper_nonoxidation_cannot_be_a_premise')
        if 'ch9-paragraph29' in topic_ids:
            require(not any('0.0002nm' in a.replace(' ', '').replace(',', '.') for a in plain_values),
                    'unreviewed_gold_leaf_unit_cannot_be_a_premise')
            require(not any('kumushli suv' in a.casefold() and 'doim' in a.casefold() for a in plain_values),
                    'unreviewed_silver_water_safety_cannot_be_a_premise')
        if 'ch9-paragraph30' in topic_ids:
            require(not any(a.replace(' ', '') == 'Zn(OH)2+H2SO4=ZnSO4+H2O' for a in f['verified_answers']),
                    'unbalanced_zinc_hydroxide_water_copy_cannot_be_an_answer')
        if 'ch9-paragraph31' in topic_ids:
            require(not any('ortiqcha HCl'.casefold() in a.casefold() and 'CrCl3' in a
                            for a in f['verified_answers']),
                    'unreviewed_chromium_excess_acid_product_cannot_be_an_answer')
        if 'ch9-paragraph32' in topic_ids:
            require(not any(a.replace(' ', '') == 'K2Cr2O7+H2SO4=CrO3+K2SO4+H2O' for a in f['verified_answers']),
                    'unbalanced_chromium_trioxide_copy_cannot_be_an_answer')
        if 'ch9-paragraph33' in topic_ids:
            require(not any('K2MnO4' in a and ('+7' in a or '3 elektron' in a.casefold())
                            for a in f['verified_answers']),
                    'unreviewed_manganate_oxidation_copy_cannot_be_an_answer')
        if 'ch9-paragraph34' in topic_ids:
            require(not any('limonit' in a.casefold() and 'FeO2' in a
                            for a in plain_values),
                    'unreviewed_limonite_formula_cannot_be_a_premise')
            require(not any('juftlashmagan' in a.casefold() and '6' in a
                            for a in f['verified_answers']),
                    'unreviewed_iron_orbital_diagram_cannot_be_an_answer')
        if 'ch9-paragraph35' in topic_ids:
            require(not any(a.replace(' ', '') in {'200mg', '6–40mg', '7–35g'}
                            for a in f['verified_answers']),
                    'unreviewed_iron_clinical_dose_cannot_be_an_answer')
        if 'ch9-paragraph37' in topic_ids:
            require(not any(a.replace(' ', '') in {'MeO+2HCl=MeCl2+H2', '2Al+3O2=2Al2O3'}
                            for a in f['verified_answers']),
                    'unbalanced_steel_worked_copy_cannot_be_an_answer')
        if 'ch9-paragraph38' in topic_ids:
            require(not any('etan' in a.casefold() and 'element' in a.casefold()
                            for a in f['verified_answers']),
                    'unreviewed_ethane_element_copy_cannot_be_an_answer')
        if 'ch9-paragraph39' in topic_ids:
            require(not any('akaritsid' in a.casefold() and 'kapalak' in a.casefold()
                            for a in f['verified_answers']),
                    'unreviewed_acaricide_taxonomy_copy_cannot_be_an_answer')
        if 'ch9-practical01' in topic_ids:
            require(not any('tuproq' in a.casefold() and 'doim' in a.casefold() and 'AgCl' in a
                            for a in f['verified_answers']),
                    'unknown_soil_precipitate_identity_cannot_be_an_answer')
        if 'ch9-practical02' in topic_ids:
            require(not any('nitrat' in a.casefold() and 'universal' in a.casefold()
                            for a in f['verified_answers']),
                    'closed_candidate_elimination_is_not_universal_nitrate_test')
        if 'ch9-laboratory02' in topic_ids:
            require(not any(re.search(r'(?i)\bMohs\s*[=:]?\s*\d', a)
                            for a in f['verified_answers']),
                    'missing_mineral_hardness_cannot_be_fabricated')
        if 'ch9-laboratory07' in topic_ids:
            require(not any('Cu anodda doim Cl2' in a for a in f['verified_answers']),
                    'unqualified_copper_anode_chlorine_key_requires_review')
        if 'ch9-laboratory10' in topic_ids:
            require(not any('barcha Al doim'.casefold() in a.casefold()
                            for a in f['verified_answers']),
                    'drop_counts_cannot_certify_complete_precipitation')
        if 'ch9-laboratory11' in topic_ids:
            require(not any('AlCl3 doim to‘liq'.casefold() in a.casefold()
                            for a in f['verified_answers']),
                    'formal_hydrolysis_is_not_unconditional_complete_conversion')
        if 'ch9-laboratory13' in topic_ids:
            require(not any('zichliksiz aniq massa' in a.casefold() for a in f['verified_answers']),
                    'missing_solution_densities_cannot_certify_mass')
        if 'ch9-laboratory16' in topic_ids:
            require(not any('yagona haqiqiy faza' in a.casefold() for a in f['verified_answers']),
                    'source_complex_notation_is_not_unique_actual_phase')
        if 'ch9-laboratory17' in topic_ids:
            require(not any('teng massa doim teng tezlik' in a.casefold() for a in f['verified_answers']),
                    'total_gas_amount_is_not_actual_rate')
        if 'ch10-paragraph01' in topic_ids:
            require(not any('barcha organik moddalar noelektrolit' in a.casefold()
                            for a in f['verified_answers']),
                    'organic_generalizations_are_not_universal_keys')
        if 'ch10-paragraph02' in topic_ids:
            require(not any('HCOOH' in a and 'sirka' in a.casefold()
                            for a in f['verified_answers']),
                    'misprinted_formic_acetic_caption_cannot_be_a_key')
        if 'ch10-paragraph03' in topic_ids:
            require(not any(a.replace(' ', '') == 'CH3CHClCH2CH2'
                            for a in f['verified_answers']),
                    'missing_terminal_hydrogen_copy_cannot_be_a_key')
        if 'ch10-paragraph04' in topic_ids:
            require(not any('faqat organik moddalar polimerlanadi' in a.casefold()
                            for a in f['verified_answers']),
                    'polymerization_universality_requires_source_review')
        if 'ch10-paragraph05' in topic_ids:
            require(not any(a.replace(',', '.') == '82.75' for a in f['verified_answers']),
                    'copied_percentage_precision_cannot_replace_declared_rounding')
        if 'ch10-paragraph06' in topic_ids:
            require(not any(a.replace(' ', '') == '1,5-dimetilgeksan' for a in f['verified_answers']),
                    'copied_nonlongest_parent_name_requires_review')
        if 'ch10-paragraph07' in topic_ids:
            require(not any('tetrametilgeksan' in a.casefold() for a in f['verified_answers']),
                    'c8_dimer_cannot_use_c10_prose_name')
        if 'ch10-paragraph08' in topic_ids:
            require(not any('pentanda c soni kamayadi' in a.casefold() for a in f['verified_answers']),
                    'same_c5_isomer_diagram_is_not_fragmentation')
        if 'ch10-paragraph09' in topic_ids:
            require(not any('har qanday alkan o‘z-o‘zidan halqa' in a.casefold() for a in f['verified_answers']),
                    'schematic_formula_difference_is_not_guaranteed_cyclization')
        if 'ch10-paragraph10' in topic_ids and 'Ma’lumotlar mos kelmaydi' in f['verified_answers']:
            require('198' not in f['verified_answers'],
                    'inconsistent_combustion_data_cannot_supply_oxygen_key')
        if 'ch10-paragraph11' in topic_ids:
            require(not any('cnh2n doim faqat alken' in a.casefold() for a in f['verified_answers']),
                    'family_composition_is_not_unique_connectivity')
        if 'ch10-paragraph12' in topic_ids:
            require(not any('e/z ustunligi faqat molekulyar massa bilan' in a.casefold()
                            for a in f['verified_answers']),
                    'unreviewed_mass_only_ez_priority_cannot_be_a_key')
        if 'ch10-paragraph13' in topic_ids:
            require(not any('barcha buten izomerlari n.sh.da gaz' in a.casefold()
                            for a in f['verified_answers']),
                    'unqualified_all_butene_phase_cannot_be_a_key')
        if 'ch10-paragraph14' in topic_ids:
            require(not any(a.replace('–', '-') == 'H2C-CH-CH=CH2' for a in f['verified_answers']),
                    'missing_diene_bond_copy_cannot_be_a_key')
        if 'ch10-paragraph15' in topic_ids:
            require(not any('pentin yagona tuzilish' in a.casefold() for a in f['verified_answers']),
                    'alkyne_gas_ratio_does_not_determine_unique_graph')
        if 'ch10-paragraph16' in topic_ids:
            require('Toluol har doim faqat tribrommahsulot'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'arene_sole_product_without_conditions_is_withheld')
        if 'ch10-paragraph17' in topic_ids:
            require('109.28'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'decimal_angle_copy_requires_review')
        if 'ch10-paragraph18' in topic_ids:
            require('Parafin va vazelin aynan bir modda'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'petroleum_product_synonym_error_is_withheld')
        if 'ch10-paragraph19' in topic_ids:
            require('22.4/67.2=3'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'reciprocal_volume_division_cannot_be_a_key')
        if 'ch10-paragraph20' in topic_ids:
            require('3-metilpentanon-1'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'terminal_ketone_misprint_is_withheld')
        if 'ch10-paragraph21' in topic_ids:
            require('140°C barcha spirtlar uchun aniq chegara'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'universal_dehydration_threshold_is_withheld')
        if 'ch10-paragraph22' in topic_ids:
            require('Bir C da ikki OH bo‘lishi mutlaqo mumkin emas'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'absolute_gemdiol_impossibility_is_withheld')
        if 'ch10-paragraph23' in topic_ids:
            require('Fe(C6H5O)3 har doim yagona kompleks'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'phenol_complex_schematic_is_not_unique_speciation')
        if 'ch10-paragraph24' in topic_ids:
            require('2-metilpropan'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'aldehyde_wrong_alkane_suffix_is_withheld')
        if 'ch10-paragraph25' in topic_ids:
            require('C6H12O yagona keton tuzilishi'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'ketone_amount_does_not_determine_unique_graph')
        if 'ch10-paragraph26' in topic_ids:
            require('2,2-metilbutan kislota'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'branched_acid_wrong_caption_is_withheld')
        if 'ch10-paragraph27' in topic_ids:
            require('Dimetilefir va metilpropilefir izomer'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'different_carbon_ether_pair_cannot_be_isomers')
        if 'ch10-paragraph28' in topic_ids:
            require('Ishqorli gidrolizda faqat erkin kislota'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'alkaline_ester_hydrolysis_requires_source_salt_products')
        if 'ch10-paragraph29' in topic_ids:
            require('Barcha o‘simlik yog‘lari suyuq'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'universal_fat_phase_claim_is_withheld')
        if 'ch10-paragraph30' in topic_ids:
            require('Fruktoza kumush ko‘zguni hech qachon bermaydi'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'unverified_sugar_redox_exclusivity_is_withheld')
        if 'ch10-paragraph31' in topic_ids:
            require('Bir molekula kraxmaldan 200 mol glukoza'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'polymer_particle_count_is_not_moles')
        if 'ch10-paragraph32' in topic_ids:
            require('Nitrolash har doim bitta sof mahsulot'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'unconditional_nitration_product_claim_is_withheld')
        if 'ch10-paragraph33' in topic_ids:
            require('C4H11N jami faqat 4 ta izomer'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'primary_amine_examples_are_not_all_amine_isomers')
        if 'ch10-paragraph34' in topic_ids:
            require('Har qanday dipeptid musbat biuret beradi'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'universal_dipeptide_biuret_claim_is_withheld')
        if 'ch10-paragraph35' in topic_ids:
            require('PVC hech qachon suyuqlanmaydi va yonmaydi'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'absolute_pvc_thermal_claim_is_withheld')
        if 'ch10-laboratory01' in topic_ids:
            require('Gazni amalda yig‘ish'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'lab_ethanol_physical_gas_collection_is_not_an_answer')
        if 'ch10-laboratory02' in topic_ids:
            require('Alanga atsetilenni yagona isbotlaydi'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'lab_acetylene_flame_is_not_unique_identity')
        if 'ch10-laboratory03' in topic_ids:
            require('Ko‘k rang har qanday ko‘p atomli spirtni isbotlaydi'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'lab_glycerol_blue_is_not_universal_identity')
        if 'ch10-laboratory04' in topic_ids:
            require('Magniy barcha sharoitda ruxdan tezroq'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'lab_acid_reported_rate_is_not_universal')
        if 'ch10-laboratory05' in topic_ids:
            require('C6H12O6+2Cu(OH)2=C6H12O7+Cu2O+H2O'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'lab_glucose_missing_water_literal_is_withheld')
        if 'ch10-laboratory06' in topic_ids:
            require('Biuret rangi oqsilni yagona isbotlaydi'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'lab_biuret_color_is_not_unique_identity')
        if 'ch11-paragraph01' in topic_ids:
            require('n² ta pog‘onacha'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'quantum_shell_n_squared_is_orbitals_not_subshells')
        if 'ch11-paragraph02' in topic_ids:
            require('Barcha elementlarning eng yuqori oksidlanishi guruh raqamiga teng'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'periodic_group_is_not_universal_max_oxidation')
        if 'ch11-paragraph03' in topic_ids:
            require('Cr51 jami 78 ta zarracha'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'isotope_cr51_wrong_particle_sum_withheld')
        if 'ch11-paragraph04' in topic_ids:
            require('Suyuq simobda metall bog‘ yo‘q'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'bond_liquid_mercury_claim_withheld')
        if 'ch11-paragraph05' in topic_ids:
            require('Ag atom massasi 1.79e-24 g'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'mole_silver_wrong_single_atom_exponent_withheld')
        if 'ch11-paragraph06' in topic_ids:
            require('Molyar hajm 22.4 mol/L'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'gas_molar_volume_reciprocal_unit_withheld')
        if 'ch11-paragraph07' in topic_ids:
            require('Ekvivalent massa reaksiyaga hech qachon bog‘liq emas'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'equivalent_requires_reaction_context')
        if 'ch11-paragraph08' in topic_ids:
            require('Birlik o‘zgarsa fizik R doimiysi o‘zgaradi'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'gas_R_physical_constant_not_changed_by_units')
        if 'ch11-paragraph09' in topic_ids:
            require('H2SO4 kuchsiz elektrolit'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'electrolyte_sulfuric_weak_literal_withheld')
        if 'ch11-paragraph10' in topic_ids:
            require('CaCl2 dan bitta xlorid ioni'.casefold() not in {a.casefold() for a in f['verified_answers']},
                    'dissociation_cacl2_chloride_count_withheld')
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
        validate_question_erratum(q, facts)
        if any(r['topic_id'] == 'ch7-paragraph24' for r in q['source_refs']):
            require(public.get('unit') not in {'kJ', 'kJ/mol'},
                    'unresolved_heat_sign_cannot_be_an_answer')
        if any(r['topic_id'] == 'ch7-7' for r in q['source_refs']):
            if q.get('response_kind') == 'numeric_value' and public.get('unit') in {'l', 'ml'}:
                from services.chemistry_grading import canonical_number
                require(canonical_number(spec['verified_answer']) not in {'22.4', '22400'},
                        'unresolved_water_vapour_state_cannot_be_an_answer')
        if any(r['topic_id'] == 'ch7-9' for r in q['source_refs']):
            if q.get('response_kind') == 'numeric_value' and public.get('unit') in {'l', 'ml'}:
                from services.chemistry_grading import canonical_number
                require(canonical_number(spec['verified_answer']) not in {'4.48', '8.96', '4480', '8960'},
                        'unresolved_review_co2_product_cannot_be_an_answer')
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
        validate_lesson(catalog, lesson, review, reviewed_context_topics=topics)
        records = {r['id']: r for b in catalog['books'] for r in b['records']}
        require(all(identifier in integrated_reviews for identifier in lesson.get('source_context_ids', [])
                    if records[identifier]['kind'] == 'review'),
                'review_context_must_already_be_integrated')
        require(lesson["key"] not in keys and lesson["topic_id"] not in topics, "duplicate_indexed_lesson")
        keys.add(lesson["key"]); topics.add(lesson["topic_id"])
        integrated_reviews.update(lesson.get('source_activity_ids', []))
        lessons.append(lesson)
    return lessons
