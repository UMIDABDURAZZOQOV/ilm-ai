"""
import_from_opensat.py — Import SAT questions from OpenSAT API.

OpenSAT API: https://pinesat.duckdns.org/api/questions
- section: english | math
- domain: filter by domain
- limit: max questions

Converts OpenSAT format to Ilm AI SAT question bank format.
"""
import requests
import time
from typing import Optional
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.db import SessionLocal, get_db
from services.models import SatIeltsQuestion
from services.question_bank import add_question, validate_question

# Domain mapping from OpenSAT to Ilm AI format
DOMAIN_MAPPING = {
    # Math
    "Algebra": "Algebra",
    "Advanced Math": "Advanced Math",
    "Problem-Solving and Data Analysis": "Problem Solving & Data Analysis",
    "Geometry and Trigonometry": "Geometry & Trigonometry",
    # Reading & Writing
    "Information and Ideas": "Information and Ideas",
    "Craft and Structure": "Craft and Structure",
    "Expression of Ideas": "Expression of Ideas",
    "Standard English Conventions": "Standard English Conventions",
}

# Skill mapping (OpenSAT uses different skill names)
SKILL_MAPPING = {
    # Math - Algebra
    "Linear equations in one variable": "Linear equations in one variable",
    "Linear functions": "Linear functions",
    "Linear equations in two variables": "Linear equations in two variables",
    "Systems of two linear equations in two variables": "Systems of two linear equations",
    "Linear inequalities in one or two variables": "Linear inequalities",
    # Math - Advanced Math
    "Nonlinear functions": "Nonlinear functions",
    "Nonlinear equations in one variable and systems of equations in two variables": "Nonlinear equations and systems",
    "Equivalent expressions": "Equivalent expressions",
    # Math - Problem Solving
    "Ratios, rates, proportional relationships, and units": "Ratios, rates, and proportions",
    "Percentages": "Percentages",
    "One-variable data: Distributions and measures of center and spread": "One-variable data",
    "Two-variable data: Models and scatterplots": "Two-variable data",
    "Probability and conditional probability": "Probability",
    "Inference from sample statistics and margin of error": "Inference from statistics",
    "Evaluating statistical claims": "Evaluating statistical claims",
    # Math - Geometry
    "Area and volume": "Area and volume",
    "Lines, angles, and triangles": "Lines, angles, and triangles",
    "Right triangles and trigonometry": "Right triangles and trigonometry",
    "Circles": "Circles",
    # Reading & Writing
    "Central Ideas and Details": "Central Ideas and Details",
    "Command of Evidence": "Command of Evidence",
    "Inferences": "Inferences",
    "Words in Context": "Words in Context",
    "Text Structure and Purpose": "Text Structure and Purpose",
    "Cross-Text Connections": "Cross-Text Connections",
    "Rhetorical Synthesis": "Rhetorical Synthesis",
    "Transitions": "Transitions",
    "Boundaries": "Boundaries",
    "Form, Structure, and Sense": "Form, Structure, and Sense",
}

# Difficulty mapping
DIFFICULTY_MAPPING = {
    "easy": "easy",
    "medium": "medium",
    "hard": "hard",
    "Easy": "easy",
    "Medium": "medium",
    "Hard": "hard",
}


def fetch_opensat_questions(section: str = "math", domain: Optional[str] = None, limit: Optional[int] = None) -> list:
    """Fetch questions from OpenSAT API."""
    url = "https://pinesat.duckdns.org/api/questions"
    params = {"section": section}
    if domain:
        params["domain"] = domain
    if limit:
        params["limit"] = limit
    
    print(f"Fetching from OpenSAT: section={section}, domain={domain}, limit={limit}")
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def convert_opensat_to_ilm(opensat_q: dict, section: str) -> dict:
    """Convert OpenSAT question format to Ilm AI format."""
    # Extract domain and skill from OpenSAT data
    domain = DOMAIN_MAPPING.get(opensat_q.get("domain", ""), "General")
    
    # Determine skill based on domain and question content
    skill = None
    if section == "math":
        # Map common math skills
        skill = SKILL_MAPPING.get(opensat_q.get("skill", ""))
        if not skill:
            # Fallback: use domain as skill
            skill = domain
    else:
        # Reading & Writing
        skill = SKILL_MAPPING.get(opensat_q.get("skill", ""))
        if not skill:
            skill = "General"
    
    # Extract question data
    q_data = opensat_q.get("question", {})
    
    # Build question text
    question_text = q_data.get("paragraph", "")
    if q_data.get("question"):
        question_text += f"\n\n{q_data['question']}"
    
    # Extract choices
    choices = q_data.get("choices", {})
    options = []
    for letter in ["A", "B", "C", "D"]:
        if letter in choices:
            options.append(f"{letter}) {choices[letter]}")
    
    # Extract correct answer
    correct_letter = q_data.get("correct_answer", "A")
    correct_answer = f"{correct_letter}) {choices.get(correct_letter, "")}"
    
    # Extract explanation
    rubric = q_data.get("explanation", "")
    
    # Determine difficulty (default to medium if not specified)
    difficulty = DIFFICULTY_MAPPING.get(opensat_q.get("difficulty", "medium"), "medium")
    
    return {
        "exam_type": "SAT",
        "domain": domain,
        "skill": skill,
        "difficulty": difficulty,
        "question_type": "mcq",
        "question_text": question_text,
        "options": options,
        "correct_answer": correct_answer,
        "rubric": rubric,
        "source_filename": "OpenSAT",
        "tags": ["SAT", domain, skill, difficulty],
    }


def import_opensat_section(section: str, db, limit_per_domain: int = 50):
    """Import questions from OpenSAT for a given section."""
    print(f"\n=== Importing {section.upper()} questions from OpenSAT ===")
    
    # Get all domains for this section
    if section == "math":
        domains = [
            "Algebra",
            "Advanced Math",
            "Problem-Solving and Data Analysis",
            "Geometry and Trigonometry",
        ]
    else:
        domains = [
            "Information and Ideas",
            "Craft and Structure",
            "Expression of Ideas",
            "Standard English Conventions",
        ]
    
    total_imported = 0
    total_failed = 0
    
    for domain in domains:
        print(f"\nFetching domain: {domain}")
        try:
            opensat_questions = fetch_opensat_questions(section=section, domain=domain, limit=limit_per_domain)
            print(f"  Retrieved {len(opensat_questions)} questions")
            
            for opensat_q in opensat_questions:
                try:
                    # Convert format
                    ilm_q = convert_opensat_to_ilm(opensat_q, section)
                    
                    # Validate
                    ok, err = validate_question(ilm_q)
                    if not ok:
                        print(f"  Validation failed: {err}")
                        total_failed += 1
                        continue
                    
                    # Check if already exists (by question_text)
                    existing = db.query(SatIeltsQuestion).filter(
                        SatIeltsQuestion.question_text == ilm_q["question_text"]
                    ).first()
                    if existing:
                        print(f"  Skipping duplicate question")
                        continue
                    
                    # Add to database
                    q = add_question(db, ilm_q)
                    print(f"  Imported question ID: {q.id}")
                    total_imported += 1
                    
                    # Small delay to avoid overwhelming DB
                    time.sleep(0.01)
                    
                except Exception as e:
                    print(f"  Error importing question: {e}")
                    total_failed += 1
                    
        except Exception as e:
            print(f"  Error fetching domain {domain}: {e}")
            total_failed += 1
    
    print(f"\n=== {section.upper()} Import Summary ===")
    print(f"Total imported: {total_imported}")
    print(f"Total failed: {total_failed}")
    
    return total_imported, total_failed


def main():
    """Main import function."""
    print("Starting OpenSAT import...")
    
    db = SessionLocal()
    try:
        # Import Math questions
        math_imported, math_failed = import_opensat_section("math", db, limit_per_domain=100)
        
        # Import Reading & Writing questions
        rw_imported, rw_failed = import_opensat_section("english", db, limit_per_domain=100)
        
        total_imported = math_imported + rw_imported
        total_failed = math_failed + rw_failed
        
        print(f"\n=== Overall Import Summary ===")
        print(f"Total imported: {total_imported}")
        print(f"Total failed: {total_failed}")
        
    finally:
        db.close()


if __name__ == "__main__":
    main()
