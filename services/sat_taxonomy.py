"""
sat_taxonomy.py — the official Digital SAT domain/skill tree.

Domain names match the strings already used in the seeded question bank
(e.g. "Problem Solving & Data Analysis" with an ampersand), so taxonomy
lookups line up with existing rows without a data migration.
"""

SAT_TAXONOMY = {
    "Reading & Writing": [
        {
            "domain": "Information and Ideas",
            "skills": [
                "Central Ideas and Details",
                "Command of Evidence",
                "Inferences",
            ],
        },
        {
            "domain": "Craft and Structure",
            "skills": [
                "Words in Context",
                "Text Structure and Purpose",
                "Cross-Text Connections",
            ],
        },
        {
            "domain": "Expression of Ideas",
            "skills": [
                "Rhetorical Synthesis",
                "Transitions",
            ],
        },
        {
            "domain": "Standard English Conventions",
            "skills": [
                "Boundaries",
                "Form, Structure, and Sense",
            ],
        },
    ],
    "Math": [
        {
            "domain": "Algebra",
            "skills": [
                "Linear equations in one variable",
                "Linear functions",
                "Linear equations in two variables",
                "Systems of two linear equations",
                "Linear inequalities",
            ],
        },
        {
            "domain": "Advanced Math",
            "skills": [
                "Nonlinear functions",
                "Nonlinear equations and systems",
                "Equivalent expressions",
            ],
        },
        {
            "domain": "Problem Solving & Data Analysis",
            "skills": [
                "Ratios, rates, and proportions",
                "Percentages",
                "One-variable data",
                "Two-variable data",
                "Probability",
                "Inference from statistics",
                "Evaluating statistical claims",
            ],
        },
        {
            "domain": "Geometry & Trigonometry",
            "skills": [
                "Area and volume",
                "Lines, angles, and triangles",
                "Right triangles and trigonometry",
                "Circles",
            ],
        },
    ],
}

IELTS_TAXONOMY = {
    "IELTS": [
        {"domain": "Listening", "skills": []},
        {"domain": "Reading", "skills": []},
        {"domain": "Writing", "skills": []},
        {"domain": "Speaking", "skills": []},
    ],
}


def get_taxonomy(exam_type: str) -> dict:
    return SAT_TAXONOMY if exam_type == "SAT" else IELTS_TAXONOMY


def get_section_domains(exam_type: str, section: str) -> list[str]:
    """All domain names belonging to a named section (e.g. 'Reading & Writing').

    Returns an empty list when the section is unknown so callers can fall back
    to an unfiltered pool rather than hard-failing."""
    tax = get_taxonomy(exam_type)
    entries = tax.get(section, [])
    return [d["domain"] for d in entries]
