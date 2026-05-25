# AI-Powered ATS Resume Screening System

An advanced resume screening system that uses **Sentence Transformers (SBERT)** and **multi-component scoring** to match resumes against job descriptions with production-level accuracy.

Unlike basic keyword matchers, this system understands **semantic meaning** — so "Machine Learning" matches "ML", and a Data Science resume scores high against a Data Science JD even if the exact words differ.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![SBERT](https://img.shields.io/badge/SBERT-MiniLM--L6--v2-orange.svg)

## How It Works

```
PDF Resume → Text Extraction → Section Parsing → Multi-Component Scoring → Ranked Results
                                                        |
                                        ┌───────────────┼───────────────┐
                                        |               |               |
                                   Semantic         Skill Match     Experience +
                                   Similarity       (taxonomy +     Education
                                   (SBERT)          synonyms)       Match
                                     40%              35%           15% + 10%
```

### Scoring Formula

```
ATS Score = (Semantic Score × 0.40) + (Skill Match × 0.35) + (Experience × 0.15) + (Education × 0.10)
```

| Component | Weight | How It Works |
|-----------|--------|-------------|
| **Semantic Similarity** | 40% | SBERT encodes resume and JD into 384-dim vectors, then computes cosine similarity. Captures meaning beyond keywords. |
| **Skill Match** | 35% | Matches 300+ skills with synonym expansion (ML→machine learning, JS→javascript). Score = matched/required. |
| **Experience** | 15% | Extracts years from date ranges, compares with JD requirements. |
| **Education** | 10% | Detects degree level (PhD > Masters > Bachelors) vs. JD requirement. |

## Tech Stack

- **ML/NLP:** Sentence Transformers (all-MiniLM-L6-v2), Scikit-learn, spaCy
- **Backend:** Flask, Python
- **PDF Processing:** PyMuPDF (fitz) with pdfplumber fallback
- **Frontend:** Bootstrap 5, Chart.js
- **Data:** Pandas, NumPy, Matplotlib

## Project Structure

```
resume_screening/
├── app.py                  # Flask web application
├── scoring_engine.py       # Multi-component ATS scoring orchestrator
├── semantic_model.py       # SBERT embedding & similarity
├── skill_extractor.py      # 300+ skill taxonomy with synonym matching
├── resume_parser.py        # Section-aware PDF parsing
├── config.py               # Centralized configuration & weights
├── utils.py                # Utility helpers
├── evaluate.py             # Batch evaluation script
├── create_pdf_resumes.py   # Generate sample PDFs for testing
├── requirements.txt        # Dependencies
├── templates/
│   └── index.html          # Dashboard UI
├── static/charts/          # Generated charts
├── resumes/                # Uploaded resumes (temp)
├── dataset/
│   ├── sample_resumes/     # 5 sample PDF resumes
│   └── resumes.csv         # Optional: Kaggle dataset for evaluation
└── README.md
```

## Setup & Installation

### Prerequisites
- Python 3.8+
- ~3 GB disk space (for PyTorch + SBERT model)

### Steps

```bash
# 1. Clone & enter project
git clone https://github.com/yourusername/resume-screening-system.git
cd resume-screening-system

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate sample test resumes (optional)
pip install fpdf2
python create_pdf_resumes.py

# 5. Run the app
python app.py
```

The first run will download the SBERT model (~22 MB). After that it's cached locally.

Open **http://127.0.0.1:5000** in your browser.

## Usage

1. **Upload** one or more PDF resumes (drag & drop supported)
2. **Paste** a job description (or click "Load Sample" for a pre-filled example)
3. Click **"Analyze & Score Resumes"**
4. View results:
   - **ATS Score** with breakdown (semantic, skills, experience, education)
   - **Matched Skills** highlighted in green
   - **Missing Skills** shown when you expand a candidate row
   - **Radar Chart** for the top candidate
   - **Bar Chart** for all candidates
5. **Export CSV** for further analysis

## Evaluation

### Using Sample Resumes
```bash
python evaluate.py
```

### Using Kaggle Dataset (500+ resumes)
1. Download from: https://www.kaggle.com/datasets/snehaanvis/resume-dataset
2. Place the CSV as `dataset/resumes.csv`
3. Run: `python evaluate.py`

The evaluation script tests:
- Same-category matches should score >50%
- Cross-category matches should score <40%
- Good discrimination gap between matched and unmatched resumes

## Why Not Just TF-IDF?

| Aspect | TF-IDF (Old) | SBERT (New) |
|--------|-------------|-------------|
| "ML" vs "Machine Learning" | ❌ Different words = 0 match | ✅ Same meaning detected |
| Short JD vs long resume | ❌ Score crushed by length mismatch | ✅ Normalized embeddings |
| Scoring range | 10-25% for strong matches | 50-85% for strong matches |
| Synonym handling | ❌ None | ✅ 60+ synonyms mapped |
| Section awareness | ❌ Flat text blob | ✅ Skills/Experience/Education parsed |

## Datasets for Training & Evaluation

| Dataset | Source | Size |
|---------|--------|------|
| Resume Classification | [Kaggle](https://www.kaggle.com/datasets/snehaanvis/resume-dataset) | 2,400+ resumes |
| Resume PDFs by Category | [Kaggle](https://www.kaggle.com/datasets/dheerajmp/resume-dataset-pdf) | 200+ PDFs |
| Resume NLP Dataset | [Kaggle](https://www.kaggle.com/datasets/yashwardhanpatil/resume-dataset) | 515 resumes |
| Job Descriptions | [HuggingFace](https://huggingface.co/datasets/jacob-hugging-face/job-descriptions) | 1,000+ JDs |

## API Access

POST to `/api/score` with multipart form data:
```bash
curl -X POST http://localhost:5000/api/score \
  -F "resumes=@resume.pdf" \
  -F "job_description=We need a Python developer..."
```

Returns JSON with full scoring breakdown.

## Configuration

All tunable parameters are in `config.py`:
- Scoring weights (semantic, skills, experience, education)
- Calibration bounds for raw cosine → percentage mapping
- Skill taxonomy (300+ skills)
- Synonym mappings (60+ abbreviations)

## Deployment

### Render
```bash
pip install gunicorn
gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120
```

### Railway
Railway auto-detects Python. Set start command to:
```bash
gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120
```

> **Note:** The first request after deployment will take ~30s to download the SBERT model. Subsequent requests are fast.

## Limitations

- PDF extraction depends on PDF structure (scanned/image PDFs won't work)
- Name extraction uses heuristics, not perfect for all formats
- Skill taxonomy covers tech roles well; other domains may need expansion
- SBERT model is English-only

## License

MIT License — feel free to use and modify.

---

Built as an advanced ML portfolio project demonstrating NLP, semantic similarity, and production-level software engineering.
