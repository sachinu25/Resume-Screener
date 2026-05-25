"""
evaluate.py - Batch evaluation script for the ATS scoring engine
Tests scoring accuracy using the Kaggle resume dataset

Usage:
    1. Download the resume dataset from Kaggle:
       https://www.kaggle.com/datasets/snehaanvis/resume-dataset
    2. Place the CSV file as dataset/resumes.csv
    3. Run: python evaluate.py

This script validates that:
    - Same-category resume+JD pairs score higher than cross-category pairs
    - Scores fall in realistic ranges (not 18% for strong matches)
    - The scoring engine differentiates between good and poor matches
"""

import os
import sys
import time
import pandas as pd
import numpy as np
from scoring_engine import score_resume
from skill_extractor import match_skills
from semantic_model import compute_calibrated_similarity, warmup


# Sample job descriptions for different categories
SAMPLE_JDS = {
    'Data Science': """Data Scientist - Machine Learning Team

We are looking for an experienced Data Scientist to join our ML team. You will build
predictive models, perform data analysis, and deploy machine learning solutions.

Requirements:
- 2+ years in data science or machine learning
- Strong Python programming skills
- Experience with Pandas, NumPy, Scikit-learn
- Knowledge of statistics, feature engineering, data visualization
- Experience with SQL databases
- Understanding of deep learning (TensorFlow/PyTorch) is a plus
- Strong communication and analytical skills

Education: Master's or PhD in Computer Science, Statistics, or related field""",

    'Web Developing': """Full Stack Web Developer

Join our engineering team to build modern web applications.

Requirements:
- 2+ years of web development experience
- Proficiency in JavaScript, HTML, CSS
- Experience with React, Angular, or Vue.js
- Backend experience with Node.js, Django, or Flask
- Knowledge of SQL and NoSQL databases
- Git version control and CI/CD
- RESTful API design

Education: Bachelor's degree in Computer Science""",

    'Java Developer': """Senior Java Developer

We need a skilled Java developer for our enterprise applications.

Requirements:
- 3+ years Java development experience
- Spring Boot and Spring Framework
- SQL databases (MySQL, PostgreSQL)
- RESTful API development
- Unit testing with JUnit
- Git, Maven/Gradle
- Docker and Kubernetes knowledge

Education: Bachelor's degree in Computer Science or related field""",

    'Python Developer': """Python Developer - Backend

Looking for a Python developer to build scalable backend systems.

Requirements:
- 2+ years Python development
- Django or Flask framework experience
- SQL databases and ORM
- REST API design
- Git version control
- Docker basics
- Testing (pytest)
- Linux command line

Education: Bachelor's in CS or equivalent experience""",

    'HR': """HR Manager - Talent Acquisition

We are hiring an HR professional to lead our recruitment efforts.

Requirements:
- 3+ years HR experience
- Talent acquisition and recruitment
- Employee relations
- HRIS systems experience
- Excellent communication skills
- Knowledge of labor laws
- Interview techniques
- Team leadership

Education: Bachelor's in Human Resources or Business""",
}


def evaluate_with_csv(csv_path='dataset/resumes.csv'):
    """
    Run evaluation using the Kaggle resume dataset CSV.
    Tests same-category vs cross-category scoring accuracy.
    """
    if not os.path.exists(csv_path):
        print(f"\n  Dataset not found at '{csv_path}'")
        print("  Download from: https://www.kaggle.com/datasets/snehaanvis/resume-dataset")
        print("  Place the CSV file in the dataset/ folder\n")
        return

    print(f"\nLoading dataset from '{csv_path}'...")
    df = pd.read_csv(csv_path)

    # The dataset has columns: 'Category' and 'Resume'
    if 'Resume' not in df.columns or 'Category' not in df.columns:
        print("  Error: Expected 'Resume' and 'Category' columns in CSV")
        return

    print(f"  Found {len(df)} resumes across {df['Category'].nunique()} categories")
    print(f"  Categories: {', '.join(df['Category'].unique()[:10])}...\n")

    # Sample resumes for evaluation (max 50 per category to keep it fast)
    categories_to_test = [c for c in SAMPLE_JDS.keys() if c in df['Category'].values]
    if not categories_to_test:
        print("  Warning: No matching categories found between dataset and sample JDs")
        print(f"  Dataset categories: {list(df['Category'].unique())}")
        categories_to_test = list(df['Category'].unique()[:3])

    print(f"Testing categories: {categories_to_test}\n")
    print("-" * 70)

    same_category_scores = []
    cross_category_scores = []

    for category in categories_to_test:
        cat_resumes = df[df['Category'] == category]['Resume'].head(20).tolist()
        jd = SAMPLE_JDS.get(category, list(SAMPLE_JDS.values())[0])

        # Same-category: resume matches JD category
        for resume_text in cat_resumes[:10]:
            score = compute_calibrated_similarity(resume_text, jd)
            same_category_scores.append(score)

        # Cross-category: random other category's JD
        other_categories = [c for c in categories_to_test if c != category]
        if other_categories:
            other_jd = SAMPLE_JDS.get(other_categories[0], list(SAMPLE_JDS.values())[-1])
            for resume_text in cat_resumes[:10]:
                score = compute_calibrated_similarity(resume_text, other_jd)
                cross_category_scores.append(score)

    # Print results
    print(f"\n{'='*55}")
    print("  EVALUATION RESULTS")
    print(f"{'='*55}\n")

    if same_category_scores:
        print(f"  Same-Category Matching (resume matches JD domain):")
        print(f"    Samples tested:  {len(same_category_scores)}")
        print(f"    Mean score:      {np.mean(same_category_scores):.1f}%")
        print(f"    Median score:    {np.median(same_category_scores):.1f}%")
        print(f"    Min/Max:         {np.min(same_category_scores):.1f}% / {np.max(same_category_scores):.1f}%")
        print(f"    Scores > 50%:    {sum(1 for s in same_category_scores if s >= 50)}/{len(same_category_scores)}")

    if cross_category_scores:
        print(f"\n  Cross-Category Matching (resume vs unrelated JD):")
        print(f"    Samples tested:  {len(cross_category_scores)}")
        print(f"    Mean score:      {np.mean(cross_category_scores):.1f}%")
        print(f"    Median score:    {np.median(cross_category_scores):.1f}%")
        print(f"    Min/Max:         {np.min(cross_category_scores):.1f}% / {np.max(cross_category_scores):.1f}%")
        print(f"    Scores < 40%:    {sum(1 for s in cross_category_scores if s < 40)}/{len(cross_category_scores)}")

    if same_category_scores and cross_category_scores:
        gap = np.mean(same_category_scores) - np.mean(cross_category_scores)
        print(f"\n  Discrimination Gap: {gap:.1f}% (higher is better)")
        if gap >= 15:
            print("  ✅ Good discrimination between matched and unmatched resumes")
        elif gap >= 8:
            print("  ⚠️  Moderate discrimination — consider tuning weights")
        else:
            print("  ❌ Poor discrimination — scoring needs improvement")

    print(f"\n{'='*55}\n")


def evaluate_with_samples():
    """
    Quick evaluation using the sample PDF resumes generated by create_pdf_resumes.py.
    """
    sample_dir = os.path.join('dataset', 'sample_resumes')
    if not os.path.exists(sample_dir):
        print(f"  Sample resumes not found in '{sample_dir}'")
        print("  Run 'python create_pdf_resumes.py' first")
        return

    pdf_files = [f for f in os.listdir(sample_dir) if f.endswith('.pdf')]
    if not pdf_files:
        print("  No PDF files found in sample directory")
        return

    # Use the sample JD
    jd = SAMPLE_JDS['Web Developing']

    print(f"\nScoring {len(pdf_files)} sample resumes against Full-Stack Web Developer JD...\n")
    print(f"{'Name':<22} {'ATS Score':>10} {'Semantic':>10} {'Skills':>10} {'Exp':>10} {'Edu':>10}")
    print("-" * 75)

    for pdf_file in sorted(pdf_files):
        pdf_path = os.path.join(sample_dir, pdf_file)
        result = score_resume(pdf_path, jd)

        print(f"{result['name']:<22} "
              f"{result['composite_score']:>9.1f}% "
              f"{result['semantic_score']:>9.1f} "
              f"{result['skill_score']:>9.1f} "
              f"{result['experience_score']:>9.1f} "
              f"{result['education_score']:>9.1f}")

    print()


if __name__ == '__main__':
    print("\n" + "=" * 55)
    print("  ATS Scoring Engine — Evaluation")
    print("=" * 55)

    # Warm up model
    warmup()

    # Run sample evaluation (always available)
    print("\n--- Sample Resume Evaluation ---")
    evaluate_with_samples()

    # Run CSV evaluation if dataset is available
    print("\n--- Dataset Evaluation ---")
    evaluate_with_csv()
