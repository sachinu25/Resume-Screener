````markdown
<div align="center">

# Smart Resume Screener (Resume-Screener)

**AI-powered ATS-style resume screening using Machine Learning + NLP.**  
Upload multiple PDF resumes, paste a job description, and get **ranked candidates** with a **transparent scoring breakdown** (semantic similarity, skills match, experience, education) plus **CSV export**.

<br/>

<!-- Badges -->
![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/License-Not%20Specified-lightgrey.svg)
![Stars](https://img.shields.io/github/stars/sachinu25/Resume-Screener?style=flat)
![Forks](https://img.shields.io/github/forks/sachinu25/Resume-Screener?style=flat)
![Issues](https://img.shields.io/github/issues/sachinu25/Resume-Screener?style=flat)
![Last Commit](https://img.shields.io/github/last-commit/sachinu25/Resume-Screener?style=flat)

<br/>

</div>

---

## Project Overview

Smart Resume Screener is a **Flask-based, ML/NLP-driven** application that evaluates candidate resumes against a job description to produce an **ATS-like match score (0–100)**.  
It combines:

- **Semantic similarity** using a Sentence-BERT model (`all-MiniLM-L6-v2`)
- **Skill extraction + matching** with a structured skill taxonomy & synonyms
- **Experience scoring** from parsed resume content
- **Education scoring** from detected education level signals

This enables recruiters and hiring teams to quickly shortlist candidates while maintaining interpretability via a clear scoring breakdown.

---

## Problem Statement

Recruiters often receive a large volume of resumes per role. Manual screening is time-consuming and inconsistent.  
This project automates initial screening by:

- Extracting resume content from PDFs
- Comparing resumes to job descriptions using ML/NLP
- Ranking candidates by a composite “ATS Match Score”
- Providing transparent, component-level explanations for each score

---

## Features

> A recruiter-friendly, production-style feature set:

- ✅ **Multi-resume PDF upload** and screening against a single job description  
- ✅ **Composite ATS score (0–100)** with weighted components  
- ✅ **Component breakdown**:
  - Semantic Similarity (SBERT)
  - Skill Match
  - Experience Match
  - Education Match
- ✅ **Candidate ranking chart** auto-generated as an image
- ✅ **CSV export** of results (`static/results.csv`)
- ✅ **JSON API** for programmatic scoring (`/api/score`)
- ✅ **Sample job description endpoint** (`/sample-jd`) for quick testing
- ✅ **Input validation** (PDF-only, job description length checks)

---

## Demo

<div align="center">

### UI Screenshots / GIFs (placeholders)

> Replace the paths below with real assets (recommended: `assets/` folder)

![Dashboard Placeholder](assets/demo-dashboard.png)  
![Results Placeholder](assets/demo-results.png)  
![Ranking Chart Placeholder](assets/demo-ranking-chart.gif)

</div>

---

## Tech Stack

| Category | Technology |
|---|---|
| Language | Python |
| Web Framework | Flask |
| NLP / Embeddings | Sentence-Transformers (SBERT) |
| NLP Utilities | spaCy, NLTK |
| PDF Parsing | PyMuPDF |
| ML / Data | scikit-learn, pandas, numpy |
| Visualization | matplotlib |
| Frontend | HTML (Jinja templates) |
| Deployment (suggested) | Docker, Gunicorn, Render/Heroku/AWS |

---

## Project Architecture

```mermaid
flowchart TD
  A[User / Recruiter] -->|Upload PDFs + Job Description| B[Flask Web App (app.py)]
  B --> C[Validation & File Handling (utils.py)]
  B --> D[Scoring Orchestrator (scoring_engine.py)]

  D --> E[Resume Parsing (resume_parser.py)]
  D --> F[Semantic Similarity (semantic_model.py)]
  D --> G[Skill Extraction & Matching (skill_extractor.py)]
  D --> H[Experience & Education Scoring (resume_parser.py)]

  D --> I[Rank + Aggregate Results]
  I --> J[Chart Generation (matplotlib)]
  I --> K[CSV Export (static/results.csv)]

  B --> L[Render UI (templates/index.html)]
  B --> M[API Response (JSON) /api/score]
  J --> N[static/charts/ranking_chart.png]
```

---

## Installation

### 1) Clone the repository
```bash
git clone https://github.com/sachinu25/Resume-Screener.git
cd Resume-Screener
```

### 2) Create & activate a virtual environment
```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
```

### 3) Install dependencies
```bash
pip install -r requirements.txt
```

### 4) (Recommended) Install spaCy model
> Your code uses `spacy>=3.7.0`. Many setups also require downloading a language model:
```bash
python -m spacy download en_core_web_sm
```

---

## Usage

### Run the web app
```bash
python app.py
```

Then open:
- `http://127.0.0.1:5000`

### Screen resumes (UI)
1. Paste a job description (recommended: meaningful JD text; very short JDs are rejected)
2. Upload one or more **PDF resumes**
3. Click screen / submit
4. View ranked results + breakdown + chart
5. Download results as CSV via **Download CSV** (route: `/download-csv`)

### Use the JSON API (programmatic scoring)

**Endpoint:** `POST /api/score`  
**Request:** `multipart/form-data` with:
- `job_description` (text)
- `resumes` (one or more PDF files)

Example using `curl`:
```bash
curl -X POST http://127.0.0.1:5000/api/score \
  -F "job_description=Looking for a Python developer with Flask and NLP experience..." \
  -F "resumes=@dataset/sample_resumes/your_resume.pdf"
```

### Inference Example (Python)
```python
import requests

url = "http://127.0.0.1:5000/api/score"
files = [
    ("resumes", open("dataset/sample_resumes/your_resume.pdf", "rb"))
]
data = {
    "job_description": "Seeking a Python developer with Flask, NLP, and ML skills."
}

resp = requests.post(url, files=files, data=data)
print(resp.json())
```

---

## Dataset

This repository includes a small sample dataset intended for testing and demos:

- `dataset/sample_job_description.txt` — example job description text
- `dataset/sample_resumes/` — sample resumes (PDFs) *(directory present)*
- `dataset/sample_resumes_text/` — text versions / extracted samples *(directory present)*

> Notes:
- For real-world use, you can supply your own resumes and job descriptions through the UI/API.
- If you use proprietary resumes, ensure compliance with privacy/security policies.

---

## Project Workflow

A complete ML/NLP project lifecycle (mapped to this project):

1. **Data Collection** → Gather resumes + job descriptions  
2. **Data Cleaning** → Normalize text, remove artifacts from PDF extraction  
3. **EDA** → Inspect common skills/keywords, resume structure patterns  
4. **Feature Engineering** → Skills taxonomy + synonym mapping, section parsing  
5. **Model Training** → Use pretrained embedding models (SBERT) and scoring logic  
6. **Evaluation** → Validate ranking quality + component scores + error handling  
7. **Deployment** → Serve via Flask UI + JSON API; add Gunicorn/Docker for production

---

## Machine Learning Models Used

| Model Name | Purpose | Performance (Current) |
|---|---|---|
| `sentence-transformers/all-MiniLM-L6-v2` | Semantic similarity between resume text and job description | *Depends on dataset; typically validated via ranking quality & similarity calibration* |
| Rule-based Skill Taxonomy + Synonyms | Extract & match skills between resume and JD | *Measured by matched/missing skill precision/recall on labeled samples (recommended)* |

> This project computes a **calibrated similarity score** and a **weighted composite ATS score**:
- Semantic: **0.40**
- Skills: **0.35**
- Experience: **0.15**
- Education: **0.10**

(Weights are configurable in `config.py`.)

---

## Results

<div align="center">

### Output Artifacts

</div>

- **Ranked candidate list** (highest match first)
- **Component breakdown** per resume:
  - semantic similarity score
  - skill match score + matched/missing skills
  - experience score (estimated years vs JD)
  - education score (level detection vs JD)
- **CSV export**: `static/results.csv`
- **Ranking chart image**: `static/charts/ranking_chart.png` (generated at runtime)

> Tip: Commit a sample chart into `assets/` for an impressive recruiter-ready README.

---

## Visualizations

Placeholders (recommended file paths):

- Correlation Heatmap: `assets/viz-correlation-heatmap.png`
- Feature Importance: `assets/viz-feature-importance.png`
- Distribution Plots: `assets/viz-distributions.png`
- Confusion Matrix: `assets/viz-confusion-matrix.png`
- ROC Curve: `assets/viz-roc-curve.png`

```text
assets/
  viz-correlation-heatmap.png
  viz-feature-importance.png
  viz-distributions.png
  viz-confusion-matrix.png
  viz-roc-curve.png
```

---

## Future Improvements

- [ ] Add **Dockerfile** + `docker-compose.yml` for one-command deployment
- [ ] Add **Gunicorn + production config** (disable debug, configure timeouts)
- [ ] Add **CI** (linting, formatting, unit tests)
- [ ] Add **type hints** + mypy checks
- [ ] Improve **skill extraction** with NER + phrase matching enhancements
- [ ] Add **role-specific skill packs** (Data Scientist, Backend, DevOps, etc.)
- [ ] Add **explainability report** per candidate (PDF/HTML summary)
- [ ] Add **evaluation notebook** with labeled data + ranking metrics (NDCG/MAP)
- [ ] Add **authentication** for multi-tenant recruiter usage
- [ ] Add persistent storage (SQLite/Postgres) for screening history

---

## Contributing

Contributions are welcome and appreciated!

1. Fork the repo
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit changes:
   ```bash
   git commit -m "Add: your feature"
   ```
4. Push to your fork:
   ```bash
   git push origin feature/your-feature
   ```
5. Open a Pull Request

**Guidelines**
- Keep PRs focused and well-described
- Add/upgrade tests when possible
- Follow existing code style and naming conventions

---

## License

This project does not currently specify a license in the repository metadata.  
**Recommendation:** Add a `LICENSE` file (MIT/Apache-2.0 are common for open-source ML projects).

---

## Author

**Sachin Upadhyay**  
GitHub: https://github.com/sachinu25

---

## Acknowledgements

- Flask community for the lightweight web framework
- Hugging Face / Sentence-Transformers for state-of-the-art embedding models
- spaCy & NLTK for NLP tooling
- scikit-learn, pandas, numpy, matplotlib for ML and analytics tooling

---
````
