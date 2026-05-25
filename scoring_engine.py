"""
scoring_engine.py - Multi-component ATS scoring engine
Combines semantic similarity, skill matching, experience, and education
into a single weighted composite score
"""

import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from config import (
    WEIGHT_SEMANTIC, WEIGHT_SKILLS, WEIGHT_EXPERIENCE, WEIGHT_EDUCATION,
    CHART_DIR,
)
from semantic_model import compute_calibrated_similarity, compute_section_similarities
from skill_extractor import match_skills
from resume_parser import (
    parse_resume, extract_experience_years, compute_experience_score,
    compute_education_score,
)


def score_resume(resume_path, jd_text):
    """
    Score a single resume against a job description.

    Returns a dict with:
        - composite_score: final weighted ATS score (0-100)
        - semantic_score: SBERT similarity component (0-100)
        - skill_score: skill match component (0-100)
        - experience_score: experience match component (0-100)
        - education_score: education match component (0-100)
        - skills_detail: matched/missing/extra skills breakdown
        - section_scores: per-section similarity scores
        - parsed: full parsed resume data
    """
    # Step 1: Parse the resume
    parsed = parse_resume(resume_path)

    if parsed['error']:
        return _error_result(parsed)

    raw_text = parsed['raw_text']
    sections = parsed['sections']

    # Step 2: Semantic similarity (full resume vs JD)
    semantic_score = compute_calibrated_similarity(raw_text, jd_text)

    # Also get per-section scores for the breakdown display
    section_scores = compute_section_similarities(sections, jd_text)

    # Step 3: Skill matching
    skills_detail = match_skills(raw_text, jd_text)
    skill_score = skills_detail['score']

    # Step 4: Experience scoring
    experience_years = parsed['experience_years']
    experience_score = compute_experience_score(experience_years, jd_text)

    # Step 5: Education scoring
    education_level = parsed['education_level']
    education_score = compute_education_score(education_level, jd_text)

    # Step 6: Compute weighted composite score
    composite = (
        semantic_score * WEIGHT_SEMANTIC +
        skill_score * WEIGHT_SKILLS +
        experience_score * WEIGHT_EXPERIENCE +
        education_score * WEIGHT_EDUCATION
    )
    composite = round(min(100, max(0, composite)), 2)

    return {
        'composite_score': composite,
        'semantic_score': round(semantic_score, 2),
        'skill_score': round(skill_score, 2),
        'experience_score': round(experience_score, 2),
        'education_score': round(education_score, 2),
        'skills_detail': skills_detail,
        'section_scores': section_scores,
        'experience_years': experience_years,
        'education_level': education_level[0],
        'name': parsed['name'],
        'filename': parsed['filename'],
        'contact': parsed['contact'],
        'error': False,
    }


def _error_result(parsed):
    """Return a zero-score result for unreadable resumes."""
    return {
        'composite_score': 0.0,
        'semantic_score': 0.0,
        'skill_score': 0.0,
        'experience_score': 0.0,
        'education_score': 0.0,
        'skills_detail': {
            'matched': [], 'missing': [], 'extra': [],
            'resume_skills': [], 'jd_skills': [],
            'resume_categorized': {}, 'jd_categorized': {},
            'score': 0, 'matched_count': 0, 'required_count': 0,
        },
        'section_scores': {},
        'experience_years': 0,
        'education_level': 'none',
        'name': parsed.get('name', 'Unknown'),
        'filename': parsed.get('filename', 'unknown'),
        'contact': {},
        'error': True,
    }


def process_resumes(resume_paths, jd_text):
    """
    Process multiple resumes against a job description.
    Returns a sorted list of results and a chart path.
    """
    results = []
    for path in resume_paths:
        result = score_resume(path, jd_text)
        results.append(result)

    # Sort by composite score (highest first)
    results.sort(key=lambda x: x['composite_score'], reverse=True)

    # Assign ranks
    for i, r in enumerate(results):
        r['rank'] = i + 1

    # Build a DataFrame for chart/CSV generation
    df = pd.DataFrame([{
        'rank': r['rank'],
        'name': r['name'],
        'filename': r['filename'],
        'score': r['composite_score'],
        'semantic_score': r['semantic_score'],
        'skill_score': r['skill_score'],
        'experience_score': r['experience_score'],
        'education_score': r['education_score'],
        'error': r['error'],
    } for r in results])

    # Generate chart
    chart_path = generate_chart(df)

    return results, df, chart_path


def generate_chart(df):
    """Generate a horizontal bar chart showing candidate rankings."""
    if df.empty:
        return None

    os.makedirs(CHART_DIR, exist_ok=True)
    chart_path = os.path.join(CHART_DIR, 'ranking_chart.png')

    valid = df[~df['error']].copy()
    if valid.empty:
        return None

    fig, ax = plt.subplots(figsize=(10, max(4, len(valid) * 0.9)))

    labels = [row['name'] for _, row in valid.iterrows()]
    scores = valid['score'].tolist()

    # Color by score range
    colors = []
    for s in scores:
        if s >= 70:
            colors.append('#22c55e')
        elif s >= 45:
            colors.append('#eab308')
        else:
            colors.append('#ef4444')

    bars = ax.barh(labels, scores, color=colors, edgecolor='#1e293b', height=0.5)

    for bar, score in zip(bars, scores):
        ax.text(bar.get_width() + 1.5, bar.get_y() + bar.get_height() / 2,
                f'{score:.1f}%', va='center', fontsize=11, fontweight='bold', color='#333')

    ax.set_xlabel('ATS Match Score (%)', fontsize=12)
    ax.set_title('Candidate Ranking', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlim(0, 110)
    ax.invert_yaxis()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='y', labelsize=11)

    plt.tight_layout()
    plt.savefig(chart_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()

    return chart_path


def export_results_csv(results, output_path='static/results.csv'):
    """Export screening results to CSV."""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        rows = []
        for r in results:
            rows.append({
                'Rank': r['rank'],
                'Candidate Name': r['name'],
                'Resume File': r['filename'],
                'ATS Score (%)': r['composite_score'],
                'Semantic Score': r['semantic_score'],
                'Skill Match Score': r['skill_score'],
                'Experience Score': r['experience_score'],
                'Education Score': r['education_score'],
                'Matched Skills': ', '.join(r['skills_detail']['matched']),
                'Missing Skills': ', '.join(r['skills_detail']['missing']),
                'Years of Experience': r['experience_years'],
            })

        pd.DataFrame(rows).to_csv(output_path, index=False)
        return output_path
    except Exception as e:
        print(f"Error exporting CSV: {e}")
        return None
