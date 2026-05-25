# 🤖 Smart Resume Screener

An AI-powered ATS Resume Screening System that intelligently matches resumes with job descriptions using Machine Learning, NLP, and Semantic Similarity.

Unlike traditional keyword matchers, this system understands the meaning of skills and technologies using SBERT embeddings.

---

##  Features

- 📄 Resume PDF Parsing
- 🧠 Semantic Matching using SBERT
- 📊 ATS Score Calculation
- 🎯 Skill Extraction & Matching
- 📈 Candidate Ranking
- 📉 Radar & Bar Chart Visualization
- 📥 CSV Export
- 🌐 Flask Web Interface
- ⚡ Fast and Accurate Resume Screening

---

## 🛠️ Tech Stack

### Machine Learning / NLP
- Sentence Transformers (SBERT)
- Scikit-learn
- spaCy
- NumPy
- Pandas

### Backend
- Python
- Flask

### Frontend
- HTML
- Bootstrap 5
- Chart.js

### PDF Processing
- PyMuPDF (fitz)
- pdfplumber

---

## 📊 ATS Scoring Formula

ATS Score =

- Semantic Similarity → 40%
- Skill Match → 35%
- Experience Match → 15%
- Education Match → 10%

---

## 📂 Project Structure

```bash
resume_screening/
│
├── app.py
├── scoring_engine.py
├── semantic_model.py
├── skill_extractor.py
├── resume_parser.py
├── requirements.txt
├── config.py
│
├── templates/
│   └── index.html
│
├── static/
│   └── charts/
│
├── resumes/
├── dataset/
└── README.md
