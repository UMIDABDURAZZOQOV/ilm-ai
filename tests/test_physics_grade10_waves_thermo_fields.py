"""Independent source-checked waves, signed heat balance and field superposition."""

from copy import deepcopy
from fractions import Fraction

import pytest
from test_physics_course import NUMERIC_ORACLES, new_answer

from services.assessment_grading import grade_answer
from services.physics_curriculum import calculation_value, load_batch, validate_batch

LABELS = {
    26: [
        "Tarqalish yo‘nalishiga parallel",
        "Bir xil fazali eng yaqin nuqtalar oralig‘ini",
        "Tebranish tarqaladigan muhit",
        "Material ichidagi nuqsonlarni tekshirish",
    ],
    27: [
        "Yo‘q, atrof-muhitdagi o‘zgarish ham hisobga olinadi",
        "Holatlar farqiga, yo‘lga emas",
        "Aon=−A",
        "Bitta manbadan boshqa o‘zgarishsiz to‘liq ish oluvchi SIKLIK mashinaga",
    ],
    28: [
        "Ichki energiya kamayishi hisobiga",
        "Nol",
        "Kelvin qiymatlari, Th>Tc>0",
        "Yo‘q, formula qaytar ideal chegarani beradi",
    ],
    29: [
        "Yonishdan keyin gaz kengayib porshenga ish berishi bilan",
        "Havo",
        "Chiqindi moddasini yo‘q qilib yubormaydi",
        "Manbadagi muayyan model va tarixiy tavsif doirasida",
    ],
    30: [
        "Barcha zaryadlarning algebraik yig‘indisi",
        "Qarama-qarshi",
        "Bir nuqta, bir xil yo‘naltirilgan o‘q va signed komponentlar",
        "Komponentlar o‘zaro tik bo‘lishi",
    ],
}
ORDERS = {
    26: ["s2", "s4", "s1", "s3"],
    27: ["s2", "s1", "s3"],
    28: ["s2", "s4", "s1", "s3"],
    29: ["s3", "s4", "s1", "s2"],
    30: ["s2", "s3", "s4", "s1"],
}


def question(seq, n):
    return deepcopy(
        load_batch("grade10_batch6")["lessons"][seq - 26]["assessments"][n - 1]
    )


@pytest.mark.parametrize("seq", range(26, 31))
def test_semantically_checked_concepts_and_orders(seq):
    l = load_batch("grade10_batch6")["lessons"][seq - 26]
    qs = [q for q in l["assessments"] if q["response_kind"] == "concept_selection"]
    assert len(qs) == len(LABELS[seq]) == 4
    for q, label in zip(qs, LABELS[seq]):
        assert label in [o["label"] for o in q["public"]["options"]]
        for o in q["public"]["options"]:
            assert grade_answer(q["grading_spec"], {"choice_id": o["id"]}) == (
                "correct" if o["label"] == label else "incorrect_concept"
            )
    q = next(q for q in l["assessments"] if q["response_kind"] == "ordering")
    assert grade_answer(q["grading_spec"], {"order": ORDERS[seq]}) == "correct"
    assert grade_answer(q["grading_spec"], {"order": ORDERS[seq][::-1]}) != "correct"


@pytest.mark.parametrize(
    "identity", [k for k in NUMERIC_ORACLES if k[0] == 10 and 26 <= k[1] <= 30]
)
def test_literal_independent_values_alternative_units_and_closed_formulas(identity):
    _, seq, n = identity
    l = load_batch("grade10_batch6")["lessons"][seq - 26]
    q = l["assessments"][n - 1]
    s = q["grading_spec"]
    a = new_answer(l, q)
    assert grade_answer(s, a) == "correct"
    for f in s["formula"]["equivalents"]:
        assert grade_answer(s, {**a, "formula": f}) == "correct"
    assert grade_answer(s, {**a, "unit": "kg"}) == "dimension_mismatch"
    assert grade_answer(s, {**a, "formula": "__import__(x)"}) != "correct"
    assert grade_answer(s, {**a, "value": "999999"}) == "out_of_tolerance"


@pytest.mark.parametrize(
    "seq,n,gi,v,u",
    [
        (26, 6, 1, "0", "Hz"),
        (26, 6, 0, "-1", "m/s"),
        (26, 7, 0, "0", "cm"),
        (26, 8, 1, "0", "cm"),
        (26, 9, 0, "0", "N"),
        (26, 9, 1, "-1", "m"),
        (26, 9, 2, "0", "kg"),
        (26, 9, 0, "20", "J"),
        (27, 7, 1, "-300", "N"),
        (27, 8, 0, "900", "K"),
        (28, 6, 0, "-350", "K"),
        (28, 7, 1, "2", "kJ"),
        (28, 7, 1, "-1", "kJ"),
        (28, 8, 1, "100", "%"),
        (28, 8, 1, "-10", "%"),
        (28, 9, 0, "0", "J"),
        (28, 10, 1, "600", "K"),
        (28, 10, 1, "0", "K"),
        (28, 10, 0, "600", "J"),
        (30, 6, 1, "-11", "N"),
        (30, 7, 1, "0", "nC"),
        (30, 8, 1, "-3", "nC"),
        (30, 8, 2, "0", "m"),
        (30, 8, 0, "1e9", "N*m2/C2"),
        (30, 9, 0, "-800", "C"),
        (30, 10, 0, "-3000", "N"),
    ],
)
def test_explicit_model_domains_and_dimensions(seq, n, gi, v, u):
    q = question(seq, n)
    q["public"]["givens"][gi].update(value=v, unit=u)
    with pytest.raises(ValueError):
        calculation_value(q)


def test_signed_zero_field_cancellation_and_orthogonal_sign_invariance():
    q = question(30, 9)
    q["public"]["givens"][1]["value"] = "800"
    assert calculation_value(q) == 0
    q = question(30, 6)
    q["public"]["givens"][0]["value"] = "11"
    assert calculation_value(q) == 0
    q = question(30, 10)
    for a, b in [("3000", "4000"), ("-3000", "-4000"), ("3000", "-4000")]:
        q["public"]["givens"][0]["value"] = a
        q["public"]["givens"][1]["value"] = b
        assert calculation_value(q) == 5000
    q["public"]["givens"][0]["value"] = "0"
    q["public"]["givens"][1]["value"] = "0"
    assert calculation_value(q) == 0


def test_first_law_sign_conventions_and_conservation_are_independent():
    # Input: Q=-700,A_by=-300; DU=-400; work-on=+300.
    assert calculation_value(question(27, 7)) == -400
    q = question(27, 9)
    q["public"]["givens"][0]["value"] = "-400"
    q["public"]["givens"][1]["value"] = "-700"
    assert calculation_value(q) == 300
    assert calculation_value(question(28, 7)) == 700
    assert calculation_value(question(28, 8)) == 1300
    assert calculation_value(question(28, 9)) == Fraction(3, 8)
    assert calculation_value(question(28, 10)) == Fraction(2, 5)
    q = question(28, 6)
    q["public"]["givens"][0]["value"] = "350"
    assert calculation_value(q) == -350  # compression work-by is negative


def test_reviewed_textbook_erratum_does_not_become_an_answer_key():
    # Original 4nC opposite charges, perpendicular distances .08/.06m.
    E1 = Fraction(9_000_000_000) * Fraction(4, 10**9) / Fraction(8, 100) ** 2
    E2 = Fraction(9_000_000_000) * Fraction(4, 10**9) / Fraction(6, 100) ** 2
    assert (E1, E2) == (5625, 10000)
    assert E1**2 + E2**2 == 131640625
    assert 11473**2 < E1**2 + E2**2 < 11474**2
    assert 750**2 != E1**2 + E2**2
    # Source112 engine key146kJ exceeds Qh60kJ; Kelvin balance gives45.23kJ.
    eta = 1 - Fraction(294, 390)
    assert eta == Fraction(16, 65)
    assert 45230 < 60000 * (1 - eta) < 45231


def test_five_source_sections_counts_offset_and_no_false_experiment_claim():
    d = load_batch("grade10_batch6")
    assert validate_batch(d) == {
        "lessons": 5, "cards": 25, "formulas": 20,
        "worked_examples": 5, "assessments": 45, "frq": 20,
    }
    for l in d["lessons"]:
        assert l["review"]["independent_subject_expert"] == "not_claimed"
        assert not l["review"]["physical_experiment_completed"]
        for r in l["source_refs"]:
            assert r["printed_pages"] == [p - 1 for p in r["pdf_pages"]]
