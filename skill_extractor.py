"""
skill_extractor.py - Advanced skill extraction with synonym support
Extracts skills from text using a taxonomy of 300+ skills and synonym mapping
"""

import re
from config import SKILL_TAXONOMY, SKILL_SYNONYMS, ALL_SKILLS


def _normalize_skill(skill_text):
    """Normalize a skill string - lowercase and strip whitespace."""
    return skill_text.lower().strip()


def _expand_synonyms(text):
    """
    Replace known abbreviations/synonyms with their canonical form.
    This way 'ML' in a resume matches 'machine learning' in a JD.
    """
    text_lower = text.lower()
    for abbrev, canonical in SKILL_SYNONYMS.items():
        # Use word boundary to avoid partial matches
        pattern = r'\b' + re.escape(abbrev) + r'\b'
        text_lower = re.sub(pattern, canonical, text_lower)
    return text_lower


def extract_skills(text):
    """
    Extract all recognized skills from a text.

    Returns:
        found_skills: list of skill strings found
        categorized: dict of category → list of skills
    """
    if not text:
        return [], {}

    # Expand synonyms first so abbreviations get matched
    expanded_text = _expand_synonyms(text)

    found_skills = []
    categorized = {}

    for category, skills in SKILL_TAXONOMY.items():
        category_matches = []
        for skill in skills:
            # Word boundary matching
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, expanded_text):
                if skill not in found_skills:
                    found_skills.append(skill)
                    category_matches.append(skill)

        if category_matches:
            categorized[category] = category_matches

    return found_skills, categorized


def extract_skills_from_jd(jd_text):
    """
    Extract required skills from a job description.
    Same as extract_skills but specifically for JD context.
    """
    return extract_skills(jd_text)


def match_skills(resume_text, jd_text):
    """
    Compare skills found in resume vs job description.

    Returns a dict with:
        - matched: skills present in both resume and JD
        - missing: skills in JD but not in resume
        - extra: skills in resume but not in JD
        - resume_skills: all skills found in resume (categorized)
        - jd_skills: all skills required by JD
        - score: match percentage (0-100)
    """
    resume_skills, resume_categorized = extract_skills(resume_text)
    jd_skills, jd_categorized = extract_skills(jd_text)

    # Also do synonym-expanded matching
    resume_expanded = set()
    for skill in resume_skills:
        resume_expanded.add(skill)
        # Check if any synonym maps to this skill
        for abbrev, canonical in SKILL_SYNONYMS.items():
            if canonical == skill:
                resume_expanded.add(abbrev)

    jd_expanded = set()
    for skill in jd_skills:
        jd_expanded.add(skill)
        for abbrev, canonical in SKILL_SYNONYMS.items():
            if canonical == skill:
                jd_expanded.add(abbrev)

    # Calculate matched and missing using canonical forms
    resume_set = set(resume_skills)
    jd_set = set(jd_skills)

    matched = sorted(list(resume_set & jd_set))
    missing = sorted(list(jd_set - resume_set))
    extra = sorted(list(resume_set - jd_set))

    # Score: what percentage of JD skills does the resume cover?
    if len(jd_set) == 0:
        score = 50.0  # No specific skills in JD? Give a neutral score
    else:
        score = (len(matched) / len(jd_set)) * 100

    return {
        'matched': matched,
        'missing': missing,
        'extra': extra,
        'resume_skills': resume_skills,
        'resume_categorized': resume_categorized,
        'jd_skills': jd_skills,
        'jd_categorized': jd_categorized,
        'score': round(score, 2),
        'matched_count': len(matched),
        'required_count': len(jd_set),
    }
