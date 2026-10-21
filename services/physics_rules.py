"""Reviewed grade-six formula families and independent SI arithmetic oracles.

No runtime evaluation of the submitted formula, no general CAS/equivalence
claim. Each alternative has a stated source domain. The content validator
recalculates answers from structured givens, independently of stored answers.
"""

from fractions import Fraction

from services.assessment_grading import UNITS, numeric


def rule(target, variables, equivalents, conditions):
    return {
        "target": target,
        "variables": variables,
        "equivalents": equivalents,
        "conditions": conditions,
    }


REVIEWED_FORMULAS = {
    "film_thickness": rule(
        "d",
        ["V", "S"],
        ["V/S", "V*S^-1"],
        "Bir molekulyar qatlam deb olingan bir tekis parda; S>0; V hajm, S yuza; PDF21. Bu model taxminiy.",
    ),
    "front_speed": rule(
        "v",
        ["h", "t"],
        ["h/t", "h*t^-1"],
        "h rangli qatlam siljishi, t>0 kuzatish vaqti; PDF28 dagi D≈h/t faqat shu kuzatuv ko‘rsatkichi, universal diffuziya koeffitsiyenti emas.",
    ),
    "kg_to_g": rule("y", ["x"], ["1000*x", "x*1000"], "x kg, y g; PDF30."),
    "g_to_kg": rule("y", ["x"], ["x/1000", "0.001*x"], "x g, y kg; PDF30."),
    "tonne_to_kg": rule("y", ["x"], ["1000*x", "x*1000"], "x t, y kg; PDF30."),
    "mass_sum3": rule(
        "m",
        ["m1", "m2", "m3"],
        ["m1+m2+m3"],
        "Muvozanatdagi tarozi: uch toshning massalari bir birlikda; PDF30–32.",
    ),
    "tare_mass": rule(
        "m",
        ["M", "m0"],
        ["M-m0"],
        "M idish va suvning umumiy massasi, m0 bo‘sh idish massasi, M>=m0; bir birlikda; PDF32.",
    ),
    "density": rule(
        "rho",
        ["m", "V"],
        ["m/V", "m*V^-1"],
        "Jismning o‘rtacha zichligi; m>0, V>0, mos massa va hajm birliklari; PDF33–35,37–38.",
    ),
    "density_mass": rule(
        "m", ["rho", "V"], ["rho*V", "V*rho"], "Bir jinsli jism: rho>0, V>0; PDF35."
    ),
    "density_volume": rule(
        "V", ["m", "rho"], ["m/rho", "m*rho^-1"], "Bir jinsli jism: rho>0, m>0; PDF35."
    ),
    "displacement": rule(
        "V",
        ["V2", "V1"],
        ["V2-V1"],
        "Jism to‘liq botgan, erimaydi, suv to‘kilmaydi, havo pufaklari yo‘q; V2>V1, bir hajm birligida; PDF34,37.",
    ),
    "box_volume": rule(
        "V",
        ["l1", "l2", "l3"],
        ["l1*l2*l3"],
        "To‘g‘ri burchakli parallelepipedning musbat o‘lchamlari bir uzunlik birligida; PDF37.",
    ),
}
DIMENSION_UNIT = {
    "length": "m",
    "time": "s",
    "mass": "kg",
    "area": "m2",
    "volume": "m3",
    "density": "kg/m3",
    "speed": "m/s",
}


def reviewed_calculation(question):
    """Exact independent arithmetic, with source/model and unit-domain checks."""
    name = question["grading_spec"]["rule"]
    givens = {g["symbol"]: g for g in question["public"]["givens"]}
    if set(givens) != set(REVIEWED_FORMULAS[name]["variables"]):
        raise ValueError("given_symbols_mismatch")

    def value(symbol, dimension):
        given = givens[symbol]
        unit = UNITS.get(given["unit"])
        amount = numeric(given["value"])
        if not unit or unit[0] != dimension or amount < 0:
            raise ValueError("given_quantity_domain")
        return amount * unit[1]

    def positive(symbol, dimension):
        result = value(symbol, dimension)
        if result <= 0:
            raise ValueError("positive_quantity_required")
        return result

    def same_units(*symbols):
        if len({givens[s]["unit"] for s in symbols}) != 1:
            raise ValueError("same_given_units_required")

    if name in {"kg_to_g", "g_to_kg", "tonne_to_kg"}:
        expected = {"kg_to_g": "kg", "g_to_kg": "g", "tonne_to_kg": "t"}[name]
        if givens["x"]["unit"] != expected:
            raise ValueError("conversion_given_unit")
        return value("x", "mass"), "mass"
    if name == "film_thickness":
        return positive("V", "volume") / positive("S", "area"), "length"
    if name == "front_speed":
        return value("h", "length") / positive("t", "time"), "speed"
    if name == "mass_sum3":
        same_units("m1", "m2", "m3")
        return sum((value(s, "mass") for s in ("m1", "m2", "m3")), Fraction()), "mass"
    if name == "tare_mass":
        same_units("M", "m0")
        result = value("M", "mass") - value("m0", "mass")
        if result < 0:
            raise ValueError("negative_tare_mass")
        return result, "mass"
    if name == "density":
        return positive("m", "mass") / positive("V", "volume"), "density"
    if name == "density_mass":
        return positive("rho", "density") * positive("V", "volume"), "mass"
    if name == "density_volume":
        return positive("m", "mass") / positive("rho", "density"), "volume"
    if name == "displacement":
        same_units("V2", "V1")
        result = value("V2", "volume") - value("V1", "volume")
        if result <= 0:
            raise ValueError("positive_displaced_volume_required")
        return result, "volume"
    if name == "box_volume":
        same_units("l1", "l2", "l3")
        return (
            positive("l1", "length")
            * positive("l2", "length")
            * positive("l3", "length")
        ), "volume"
    raise ValueError("unreviewed_formula_rule")
