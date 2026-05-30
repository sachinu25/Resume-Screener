<div align="center">

<!-- Logo Placeholder -->
<img src="assets/logo.png" alt="Smart Resume Screener Logo" width="120" height="120" />

# Smart Resume Screener

### AI-powered ATS-style Resume Screening using Machine Learning + NLP

Upload PDF resumes, paste a Job Description, and instantly receive **ranked candidates** with a transparent **ATS score breakdown** and **CSV export**.

<br/>

<!-- Badges (Dark-theme friendly) -->

![Version](https://img.shields.io/badge/version-1.0.0-black)
![Python](https://img.shields.io/badge/python-3.8%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-2ea44f)
![Stars](https://img.shields.io/github/stars/sachinu25/Resume-Screener?style=flat&color=black)
![Forks](https://img.shields.io/github/forks/sachinu25/Resume-Screener?style=flat&color=black)
![Issues](https://img.shields.io/github/issues/sachinu25/Resume-Screener?style=flat&color=black)
![Last Commit](https://img.shields.io/github/last-commit/sachinu25/Resume-Screener?style=flat&color=black)

</div>

---

# Project Preview

| Dashboard | Prediction | Analytics |
|----------|------------|----------|
| ![Dashboard](assets/preview-dashboard.png) | ![Prediction](assets/preview-prediction.png) | ![Analytics](assets/preview-analytics.png) |

---

# Problem Statement

Hiring teams receive hundreds of resumes per opening. Manual screening is slow, inconsistent, and often biased toward keyword-heavy resumes.

Smart Resume Screener solves this by:
- **Understanding meaning** using semantic embeddings (SBERT) instead of simple keyword matching.
- **Extracting skills, experience, and education signals** from resumes.
- Providing a **transparent ATS score (0–100)** so recruiters can shortlist faster.

✅ **Real-world impact:** Faster hiring cycles, improved candidate-job alignment, and more consistent screening.

---

# Key Features

| Feature | Description |
|--------|-------------|
| Semantic Similarity Scoring | SBERT embeddings compute meaning-based resume ↔ JD similarity |
| Skill Extraction & Matching | Matches required skills and highlights missing ones |
| ATS Composite Score | Weighted score combining semantic, skills, experience, education |
| Candidate Ranking | Automatically ranks resumes and generates chart visualizations |
| CSV Export | Download all results as a structured CSV for recruiter workflows |
| API Support | `/api/score` endpoint for programmatic integrations |

---

# System Architecture

```mermaid
flowchart TD
  U[Recruiter/User] --> F[Flask UI]
  F --> API[Backend API]
  API --> P[Resume Parser]
  API --> M[ML/NLP Scoring Engine]
  M --> S[SBERT Semantic Model]
  M --> K[Skill Extractor]
  M --> X[Experience + Education Scorer]
  API --> R[Results + Ranking]
  R --> V[Charts + Visualizations]
  R --> C[CSV Export]
```

---

# Complete Workflow

```mermaid
flowchart TD
  A[Dataset] --> B[Data Cleaning]
  B --> C[EDA]
  C --> D[Feature Engineering]
  D --> E[Model Training]
  E --> F[Model Evaluation]
  F --> G[Model Selection]
  G --> H[Deployment]
  H --> I[Prediction]
```

---

# Technology Stack

| Category | Technologies |
|---------|--------------|
| Programming | Python |
| ML / NLP | scikit-learn, sentence-transformers, spaCy, NLTK |
| Data | pandas, numpy |
| Visualization | matplotlib |
| Deployment | Flask (Gunicorn recommended) |
| PDF Processing | PyMuPDF |

---

# Folder Structure

```text
Resume-Screener/
├── app.py
├── config.py
├── scoring_engine.py
├── semantic_model.py
├── resume_parser.py
├── skill_extractor.py
├── utils.py
├── requirements.txt
├── dataset/
│   ├── sample_job_description.txt
│   ├── sample_resumes/
│   └── sample_resumes_text/
├── resumes/
├── static/
│   ├── results.csv
│   └── charts/
├── templates/
│   └── index.html
└── README.md
```

---

# Dataset Information

This project includes demo sample data:

| File/Folder | Description |
|------------|-------------|
| `dataset/sample_job_description.txt` | Example job description for testing |
| `dataset/sample_resumes/` | Sample resumes in PDF format |
| `dataset/sample_resumes_text/` | Text-based resume samples |

> In production, the system accepts recruiter-provided job descriptions and resumes.

---

# Exploratory Data Analysis

<details>
<summary><strong>Missing Values Analysis</strong></summary>

![Missing Values](assets/eda-missing-values.png)

</details>

<details>
<summary><strong>Correlation Analysis</strong></summary>

![Heatmap](assets/eda-heatmap.png)

</details>

<details>
<summary><strong>Outlier Detection</strong></summary>

![Pairplot](assets/eda-pairplot.png)

</details>

<details>
<summary><strong>Feature Distribution</strong></summary>

![Distribution Plot](assets/eda-distribution.png)

</details>

---

# Machine Learning Pipeline

```mermaid
flowchart TD
  A[Raw Data] --> B[Preprocessing]
  B --> C[Feature Engineering]
  C --> D[Model Training]
  D --> E[Hyperparameter Tuning]
  E --> F[Evaluation]
  F --> G[Deployment]
```

---

# Models Evaluated

| Model | Accuracy | Precision | Recall | F1 Score |
|------|----------|----------|--------|----------|
| Logistic Regression | x | x | x | x |
| Random Forest | x | x | x | x |
| XGBoost | x | x | x | x |

✅ **Best Model:** SBERT-based semantic similarity + weighted composite ATS scoring.

---

# Performance Dashboard

| Metric | Score |
|-------|------|
| Accuracy | **x** |
| Precision | **x** |
| Recall | **x** |
| F1 Score | **x** |
| ROC-AUC | **x** |

---

# Results Visualization

| Confusion Matrix | ROC Curve |
|----------------|-----------|
| ![Confusion Matrix](assets/confusion-matrix.png) | ![ROC](assets/roc-curve.png) |

| Precision-Recall Curve | Feature Importance |
|------------------------|------------------|
| ![PR Curve](assets/pr-curve.png) | ![Feature Importance](assets/feature-importance.png) |

| Learning Curve | Residual Plot |
|--------------|--------------|
| ![Learning Curve](assets/learning-curve.png) | ![Residual Plot](assets/residual-plot.png) |

---

# API Endpoints

| Method | Endpoint | Description |
|-------|----------|-------------|
| POST | `/api/score` | Score resumes against job description (JSON output) |
| GET | `/sample-jd` | Get sample job description |
| GET | `/download-csv` | Download results as CSV |

---

# Installation

```bash
git clone https://github.com/sachinu25/Resume-Screener.git
cd Resume-Screener
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

---

# Usage

Run the app locally:
```bash
python app.py
```

Open: `http://127.0.0.1:5000`

---

# Deployment

Production deployment (recommended):
```bash
pip install gunicorn
gunicorn -w 2 -b 0.0.0.0:5000 app:app
```

---

# Future Improvements

- [ ] Add Docker support
- [ ] Add CI/CD pipeline
- [ ] Improve skill extraction with deep NLP
- [ ] Add persistence layer (PostgreSQL)
- [ ] Add authentication for recruiter dashboards

---

# Contributors

Contributions are welcome! Please open an Issue or Pull Request.

---

# License

MIT License *(Recommended: Add a LICENSE file)*

---

# Contact

| Name | Role | Contact |
|------|------|---------|
| Sachin Upadhyay | Maintainer | [GitHub](https://github.com/sachinu25) |
