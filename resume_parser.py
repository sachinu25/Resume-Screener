"""
resume_parser.py - Section-aware resume parsing
Extracts structured data from PDF resumes using PyMuPDF and regex heuristics
"""

import re
import os
from config import SECTION_HEADERS, EDUCATION_LEVELS


def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF using PyMuPDF (fitz).
    Falls back to pdfplumber if PyMuPDF fails.
    """
    text = ""
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text() + "\n"
        doc.close()
    except Exception as e:
        print(f"PyMuPDF failed for '{pdf_path}': {e}")
        # Fallback to pdfplumber
        try:
            import pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e2:
            print(f"pdfplumber also failed: {e2}")
            return ""

    return text.strip()


def extract_candidate_name(text):
    """
    Extract candidate name from the first few lines of resume text.
    Uses heuristics: name is usually the first short line with mostly letters.
    """
    if not text:
        return "Unknown Candidate"

    lines = text.strip().split('\n')

    for line in lines[:8]:
        line = line.strip()
        if not line or len(line) < 2:
            continue

        # Skip lines that are clearly not names
        skip_keywords = [
            'resume', 'curriculum', 'vitae', 'cv', 'objective',
            'summary', 'experience', 'education', '@', 'http',
            'phone', 'email', 'address', 'linkedin', 'github',
            'portfolio', 'website', 'tel:', 'cell:', 'mobile',
        ]
        if any(kw in line.lower() for kw in skip_keywords):
            continue

        # Skip lines with too many digits (phone, dates, addresses)
        digit_ratio = sum(c.isdigit() for c in line) / max(len(line), 1)
        if digit_ratio > 0.2:
            continue

        # Skip long lines (paragraphs)
        if len(line) > 45:
            continue

        # Name should be 1-4 words, mostly alphabetic
        words = line.split()
        if 1 <= len(words) <= 5:
            alpha_ratio = sum(c.isalpha() or c.isspace() for c in line) / max(len(line), 1)
            if alpha_ratio > 0.8:
                # Clean up and title-case
                name = ' '.join(w.strip(',.:;') for w in words if len(w) > 0)
                name = name.title()
                if len(name) > 2:
                    return name

    return "Unknown Candidate"


def extract_contact_info(text):
    """Extract email and phone from resume text."""
    info = {'email': None, 'phone': None}

    # Email
    email_match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
    if email_match:
        info['email'] = email_match.group()

    # Phone (various formats)
    phone_match = re.search(
        r'[\+]?[\d]{0,3}[\s.-]?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}', text
    )
    if phone_match:
        info['phone'] = phone_match.group().strip()

    return info


def segment_sections(text):
    """
    Split resume text into sections based on common headers.
    Returns a dict like: {'summary': '...', 'experience': '...', 'skills': '...', ...}
    """
    if not text:
        return {}

    sections = {}
    lines = text.split('\n')
    current_section = 'header'  # Everything before the first recognized section
    current_content = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            current_content.append('')
            continue

        # Check if this line is a section header
        detected_section = _detect_section_header(stripped)

        if detected_section:
            # Save the previous section
            if current_content:
                section_text = '\n'.join(current_content).strip()
                if section_text:
                    sections[current_section] = section_text
            current_section = detected_section
            current_content = []
        else:
            current_content.append(line)

    # Don't forget the last section
    if current_content:
        section_text = '\n'.join(current_content).strip()
        if section_text:
            sections[current_section] = section_text

    return sections


def _detect_section_header(line):
    """
    Check if a line is a section header.
    Returns the canonical section name or None.
    """
    # Clean the line for comparison
    cleaned = line.lower().strip()
    cleaned = re.sub(r'[^a-z\s]', '', cleaned).strip()

    if not cleaned or len(cleaned) > 40:
        return None

    # Check against known section headers
    for section_name, headers in SECTION_HEADERS.items():
        for header in headers:
            if cleaned == header or cleaned.startswith(header + ' '):
                return section_name

    return None


def extract_experience_years(text):
    """
    Try to estimate total years of experience from resume text.
    Looks for patterns like "X years", "X+ years", date ranges in work sections.
    """
    if not text:
        return 0

    text_lower = text.lower()
    years = 0

    # Pattern 1: Explicit "X years of experience" or "X+ years experience"
    exp_pattern = re.findall(
        r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s+)?(?:experience|exp|professional|work|industry)',
        text_lower
    )
    if exp_pattern:
        years = max(int(y) for y in exp_pattern)

    # Pattern 2: Count date ranges, but only from experience-related sections
    # We look for date ranges near job-related words to avoid counting education/club dates
    if years == 0:
        # Split text into lines and look for date ranges near work context
        lines = text_lower.split('\n')
        in_experience_section = False
        total_years = 0

        work_indicators = [
            'engineer', 'developer', 'manager', 'analyst', 'scientist',
            'designer', 'intern', 'lead', 'architect', 'consultant',
            'specialist', 'coordinator', 'director', 'associate',
            'inc', 'ltd', 'llc', 'corp', 'pvt', 'solutions', 'technologies',
        ]

        for i, line in enumerate(lines):
            stripped = line.strip()
            # Detect if we're entering/leaving experience section
            if any(h in stripped for h in ['experience', 'employment', 'work history', 'career']):
                in_experience_section = True
                continue
            if any(h in stripped for h in ['education', 'certification', 'project', 'extracurricular', 'volunteer', 'award']):
                in_experience_section = False
                continue

            # Look for date ranges in this line
            date_match = re.findall(
                r'(?:(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s+)?(\d{4})\s*[-\u2013\u2014]+\s*(?:(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s+)?(\d{4}|present|current|now)',
                line
            )
            if not date_match:
                continue

            # Only count if in experience section OR line has work-related words
            context = ' '.join(lines[max(0, i-1):i+2])  # check surrounding lines
            is_work_context = in_experience_section or any(w in context for w in work_indicators)

            if is_work_context:
                for start, end in date_match:
                    start_year = int(start)
                    if end in ('present', 'current', 'now'):
                        end_year = 2026
                    else:
                        end_year = int(end)
                    if 1990 <= start_year <= 2026 and start_year <= end_year <= 2030:
                        total_years += (end_year - start_year)

        years = total_years

    return min(years, 40)


def extract_education_level(text):
    """
    Detect the highest education level mentioned in the text.
    Returns a tuple: (level_name, level_score)

    Handles abbreviated degrees like M.S., B.S., B.E., B.Tech, Ph.D.
    Uses flexible matching since \b word boundary fails with dots.
    """
    if not text:
        return ('none', 0)

    text_lower = text.lower()
    # Normalize common degree formats: "M.S." → "m.s.", "B. Tech" → "b.tech"
    text_normalized = re.sub(r'\b([bm])\.\s*([a-z])', r'\1.\2', text_lower)

    best_level = ('none', 0)

    for keyword, score in EDUCATION_LEVELS.items():
        # For keywords with dots (like 'm.s.', 'b.tech'), use looser matching
        if '.' in keyword:
            # Match with optional dots and spaces: m.s. matches M.S., MS, M. S.
            flexible = keyword.replace('.', '\\.?\\s*')
            pattern = r'(?:^|[\s(,])' + flexible + r'(?:[\s),.]|$)'
        else:
            pattern = r'\b' + re.escape(keyword) + r'(?:s|\'s)?\b'

        if re.search(pattern, text_normalized):
            if score > best_level[1]:
                best_level = (keyword, score)

    return best_level


def compute_experience_score(resume_years, jd_text):
    """
    Score how well the candidate's experience matches the JD requirements.

    Logic:
    - Extract required years from JD (e.g., "3+ years")
    - Compare with resume's actual years
    - Full marks if resume_years >= required_years
    - Partial credit if close
    """
    # Try to find required years in JD
    required_years = 0
    jd_lower = jd_text.lower()

    req_match = re.findall(r'(\d+)\+?\s*(?:years?|yrs?)', jd_lower)
    if req_match:
        required_years = max(int(y) for y in req_match)

    if required_years == 0:
        # JD doesn't specify years, give decent score based on having any experience
        if resume_years >= 5:
            return 90.0
        elif resume_years >= 2:
            return 70.0
        elif resume_years >= 1:
            return 50.0
        else:
            return 30.0

    # Compare actual vs required
    if resume_years >= required_years:
        return 100.0
    elif resume_years >= required_years * 0.7:
        return 75.0
    elif resume_years >= required_years * 0.4:
        return 50.0
    elif resume_years > 0:
        return 30.0
    else:
        return 10.0


def compute_education_score(resume_edu_level, jd_text):
    """
    Score how well education matches the JD requirement.
    """
    jd_edu_name, jd_edu_score = extract_education_level(jd_text)
    resume_name, resume_score = resume_edu_level

    if jd_edu_score == 0:
        # JD doesn't mention education requirement
        if resume_score >= 3:
            return 85.0  # Has a degree, that's good
        elif resume_score >= 1:
            return 60.0
        else:
            return 40.0

    # Compare levels
    if resume_score >= jd_edu_score:
        return 100.0
    elif resume_score >= jd_edu_score - 1:
        return 70.0
    elif resume_score > 0:
        return 40.0
    else:
        return 15.0


def parse_resume(pdf_path):
    """
    Full resume parsing pipeline.
    Returns a structured dict with all extracted info.
    """
    raw_text = extract_text_from_pdf(pdf_path)

    if not raw_text:
        return {
            'raw_text': '',
            'name': 'Could not read',
            'contact': {},
            'sections': {},
            'experience_years': 0,
            'education_level': ('none', 0),
            'filename': os.path.basename(pdf_path),
            'error': True,
        }

    name = extract_candidate_name(raw_text)
    contact = extract_contact_info(raw_text)
    sections = segment_sections(raw_text)
    experience_years = extract_experience_years(raw_text)
    education_level = extract_education_level(raw_text)

    return {
        'raw_text': raw_text,
        'name': name,
        'contact': contact,
        'sections': sections,
        'experience_years': experience_years,
        'education_level': education_level,
        'filename': os.path.basename(pdf_path),
        'error': False,
    }
