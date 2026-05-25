"""
semantic_model.py - Sentence Transformer model for semantic similarity
Uses all-MiniLM-L6-v2 to generate embeddings and compute calibrated similarity scores
"""

import numpy as np
from config import SBERT_MODEL_NAME, CALIBRATION_MIN, CALIBRATION_MAX

# Global model instance (loaded lazily on first use)
_model = None


def _get_model():
    """
    Lazy-load the sentence transformer model.
    Only downloads/loads once, then reuses the same instance.
    """
    global _model
    if _model is None:
        print(f"Loading SBERT model '{SBERT_MODEL_NAME}'... (first time only)")
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(SBERT_MODEL_NAME)
        print("Model loaded successfully.")
    return _model


def encode_text(text):
    """
    Convert text to a 384-dimensional embedding vector.
    Returns a numpy array.
    """
    if not text or not text.strip():
        return np.zeros(384)

    model = _get_model()
    embedding = model.encode(text, convert_to_numpy=True, show_progress_bar=False)
    return embedding


def compute_similarity(text_a, text_b):
    """
    Compute cosine similarity between two texts using SBERT embeddings.
    Returns a raw cosine similarity value between -1 and 1.
    """
    if not text_a or not text_b:
        return 0.0

    model = _get_model()

    embeddings = model.encode([text_a, text_b], convert_to_numpy=True,
                              show_progress_bar=False)

    # Cosine similarity
    dot_product = np.dot(embeddings[0], embeddings[1])
    norm_a = np.linalg.norm(embeddings[0])
    norm_b = np.linalg.norm(embeddings[1])

    if norm_a == 0 or norm_b == 0:
        return 0.0

    similarity = dot_product / (norm_a * norm_b)
    return float(similarity)


def compute_calibrated_similarity(text_a, text_b):
    """
    Compute similarity and calibrate it to a 0-100 score range.

    Raw SBERT cosine similarity for resume-JD pairs typically falls in [0.15, 0.70].
    This function maps that range to [0, 100] so scores feel realistic.

    A strong match (raw 0.55+) → 70-100%
    A decent match (raw 0.35-0.55) → 35-70%
    A weak match (raw < 0.25) → 0-20%
    """
    raw_sim = compute_similarity(text_a, text_b)
    return calibrate_score(raw_sim)


def calibrate_score(raw_cosine):
    """Map raw cosine similarity to a 0-100 scale using configured bounds."""
    if raw_cosine <= CALIBRATION_MIN:
        return 0.0
    if raw_cosine >= CALIBRATION_MAX:
        return 100.0

    calibrated = (raw_cosine - CALIBRATION_MIN) / (CALIBRATION_MAX - CALIBRATION_MIN) * 100
    return round(calibrated, 2)


def compute_section_similarities(resume_sections, jd_text):
    """
    Compare individual resume sections against the JD separately.
    This gives more nuanced scoring than comparing the full resume blob.

    Args:
        resume_sections: dict like {'skills': '...', 'experience': '...', ...}
        jd_text: job description text

    Returns:
        dict of section_name → calibrated similarity score
    """
    results = {}
    for section_name, section_text in resume_sections.items():
        if section_text and section_text.strip():
            raw_sim = compute_similarity(section_text, jd_text)
            results[section_name] = calibrate_score(raw_sim)
        else:
            results[section_name] = 0.0

    return results


def warmup():
    """Pre-load the model so the first request isn't slow."""
    _get_model()
    print("SBERT model warmed up and ready.")
