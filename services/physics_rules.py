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
    "km_to_m": rule("y", ["x"], ["1000*x", "x*1000"], "x km, y m; PDF47."),
    "min_to_s": rule("y", ["x"], ["60*x", "x*60"], "x minut, y sekund; PDF47."),
    "hour_to_s": rule("y", ["x"], ["3600*x", "x*3600"], "x soat, y sekund; PDF47."),
    "step_distance": rule(
        "s",
        ["l", "n"],
        ["l*n", "n*l"],
        "l o‘rtacha qadam uzunligi, n musbat butun qadamlar soni; taxminiy masofa; PDF48.",
    ),
    "motion_speed": rule(
        "v",
        ["s", "t"],
        ["s/t", "s*t^-1"],
        "s yo‘l, t>0 vaqt; tekis harakat tezligi yoki butun yo‘l/butun vaqt o‘rtachasi; PDF49–50.",
    ),
    "motion_distance": rule(
        "s",
        ["v", "t"],
        ["v*t", "t*v"],
        "v tekis harakat tezligi, t vaqt; yoki butun oraliqning berilgan o‘rtacha tezligi; PDF51.",
    ),
    "motion_time": rule(
        "t", ["s", "v"], ["s/v", "s*v^-1"], "s yo‘l, v>0 tezlik; PDF51,3-mashq7."
    ),
    "two_stage_speed": rule(
        "v",
        ["s1", "s2", "t1", "t2"],
        ["(s1+s2)/(t1+t2)"],
        "Ikki ketma-ket bosqich, yo‘llar o‘zaro va vaqtlar o‘zaro bir birlikda; umumiy yo‘l/umumiy vaqt; PDF50.",
    ),
    "earth_weight": rule(
        "F",
        ["m", "g"],
        ["m*g", "g*m"],
        "Yer sirtidagi og‘irlik kuchi moduli, g=9,81 N/kg masalada ochiq beriladi; PDF54.",
    ),
    "weight_mass": rule(
        "m",
        ["F", "g"],
        ["F/g", "F*g^-1"],
        "F og‘irlik kuchi, g=9,81 N/kg; massani topish; PDF54–55.",
    ),
    "pressure": rule(
        "p",
        ["F", "S"],
        ["F/S", "F*S^-1"],
        "F sirtga tik kuch, S>0 tegish yuzasi; o‘rtacha bosim; PDF57–58.",
    ),
    "pressure_force": rule(
        "F", ["p", "S"], ["p*S", "S*p"], "Bir tekis bosim p, yuza S; PDF57–59."
    ),
    "pressure_area": rule(
        "S",
        ["F", "p"],
        ["F/p", "F*p^-1"],
        "Tik kuch F, musbat bosim p; PDF59,5-mashq1.",
    ),
    "rectangle_area": rule(
        "S",
        ["a", "b"],
        ["a*b", "b*a"],
        "To‘g‘ri to‘rtburchakning musbat tomonlari bir uzunlik birligida; PDF58.",
    ),
    "hydraulic_force": rule(
        "F2",
        ["F1", "S1", "S2"],
        ["F1*S2/S1", "S2/S1*F1", "F1*(S2/S1)"],
        "Ideal gidravlik press, ishqalanish va sath farqi e’tiborsiz; S1>0, S2>0 bir yuza birligida; PDF60–61.",
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
    "force": "N",
    "pressure": "Pa",
    "force_per_mass": "N/kg",
    "dimensionless": "1",
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

    if name in {"km_to_m", "min_to_s", "hour_to_s"}:
        unit, dimension = {
            "km_to_m": ("km", "length"),
            "min_to_s": ("min", "time"),
            "hour_to_s": ("h", "time"),
        }[name]
        if givens["x"]["unit"] != unit:
            raise ValueError("conversion_given_unit")
        return value("x", dimension), dimension
    if name == "step_distance":
        steps = positive("n", "dimensionless")
        if steps.denominator != 1:
            raise ValueError("integer_step_count_required")
        return positive("l", "length") * steps, "length"
    if name == "motion_speed":
        return value("s", "length") / positive("t", "time"), "speed"
    if name == "motion_distance":
        return value("v", "speed") * value("t", "time"), "length"
    if name == "motion_time":
        return value("s", "length") / positive("v", "speed"), "time"
    if name == "two_stage_speed":
        same_units("s1", "s2")
        same_units("t1", "t2")
        distance = value("s1", "length") + value("s2", "length")
        duration = positive("t1", "time") + positive("t2", "time")
        return distance / duration, "speed"
    if name in {"earth_weight", "weight_mass"}:
        gravity = positive("g", "force_per_mass")
        if gravity != Fraction(981, 100):
            raise ValueError("grade6_source_gravity_is_9_81")
        if name == "earth_weight":
            return positive("m", "mass") * gravity, "force"
        return positive("F", "force") / gravity, "mass"
    if name == "pressure":
        return value("F", "force") / positive("S", "area"), "pressure"
    if name == "pressure_force":
        return value("p", "pressure") * positive("S", "area"), "force"
    if name == "pressure_area":
        return positive("F", "force") / positive("p", "pressure"), "area"
    if name == "rectangle_area":
        same_units("a", "b")
        return positive("a", "length") * positive("b", "length"), "area"
    if name == "hydraulic_force":
        same_units("S1", "S2")
        return value("F1", "force") * positive("S2", "area") / positive(
            "S1", "area"
        ), "force"

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
