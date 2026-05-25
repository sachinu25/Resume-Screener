"""
utils.py - General utility functions
Lightweight helpers used across the application
"""

import os


def validate_pdf(filename):
    """Check if the uploaded file has a PDF extension."""
    if not filename:
        return False
    return filename.lower().endswith('.pdf')


def format_score(score):
    """Format a score value for display."""
    if score is None:
        return "N/A"
    return f"{score:.1f}%"


def get_score_class(score):
    """Return a CSS class name based on score range."""
    if score >= 70:
        return 'score-high'
    elif score >= 45:
        return 'score-medium'
    else:
        return 'score-low'


def get_rank_class(rank):
    """Return a CSS class for rank badge styling."""
    if rank == 1:
        return 'rank-1'
    elif rank == 2:
        return 'rank-2'
    elif rank == 3:
        return 'rank-3'
    else:
        return 'rank-other'


def ensure_directories():
    """Create necessary directories if they don't exist."""
    dirs = ['resumes', 'static/charts', 'dataset']
    for d in dirs:
        os.makedirs(d, exist_ok=True)
