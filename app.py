"""
app.py - Flask web application for the AI-Powered ATS Screening System
Handles file uploads, resume processing, and result rendering
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
from werkzeug.utils import secure_filename
from scoring_engine import process_resumes, export_results_csv
from utils import validate_pdf, ensure_directories
from config import UPLOAD_FOLDER, FLASK_SECRET_KEY, MAX_UPLOAD_SIZE

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_UPLOAD_SIZE

# Create required directories
ensure_directories()


@app.route('/', methods=['GET'])
def index():
    """Render the main dashboard page."""
    return render_template('index.html')


@app.route('/screen', methods=['POST'])
def screen_resumes():
    """
    Handle resume screening:
    1. Validate uploads & JD
    2. Score each resume using the multi-component engine
    3. Render results with full breakdown
    """
    job_description = request.form.get('job_description', '').strip()

    if not job_description:
        flash('Please enter a job description.', 'error')
        return redirect(url_for('index'))

    if len(job_description) < 20:
        flash('Job description is too short. Please provide more detail for accurate matching.', 'error')
        return redirect(url_for('index'))

    # Handle file uploads
    files = request.files.getlist('resumes')
    if not files or all(f.filename == '' for f in files):
        flash('Please upload at least one resume PDF.', 'error')
        return redirect(url_for('index'))

    # Clear previous uploads
    for old_file in os.listdir(UPLOAD_FOLDER):
        old_path = os.path.join(UPLOAD_FOLDER, old_file)
        if os.path.isfile(old_path):
            os.remove(old_path)

    # Save uploaded files
    saved_paths = []
    for file in files:
        if file and file.filename:
            if not validate_pdf(file.filename):
                flash(f'Skipped "{file.filename}" — only PDF files are accepted.', 'warning')
                continue
            filename = secure_filename(file.filename)
            if not filename:
                continue
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            saved_paths.append(filepath)

    if not saved_paths:
        flash('No valid PDF files were uploaded.', 'error')
        return redirect(url_for('index'))

    # Run the scoring engine
    try:
        results, df, chart_path = process_resumes(saved_paths, job_description)
    except Exception as e:
        import traceback
        traceback.print_exc()
        flash(f'Error processing resumes: {str(e)}', 'error')
        return redirect(url_for('index'))

    # Generate CSV for download
    csv_path = export_results_csv(results)

    # Chart URL
    chart_url = None
    if chart_path and os.path.exists(chart_path):
        chart_url = '/' + chart_path.replace('\\', '/')

    return render_template(
        'index.html',
        results=results,
        job_description=job_description,
        chart_url=chart_url,
        csv_available=(csv_path is not None),
        total_resumes=len(saved_paths),
    )


@app.route('/download-csv')
def download_csv():
    """Download screening results as CSV."""
    csv_path = os.path.join('static', 'results.csv')
    if os.path.exists(csv_path):
        return send_file(csv_path, as_attachment=True, download_name='ats_screening_results.csv')
    flash('No results available to download.', 'error')
    return redirect(url_for('index'))


@app.route('/sample-jd')
def sample_job_description():
    """Return a sample job description for testing."""
    sample_jd = """Senior Software Engineer — Full Stack Development

We are looking for a Senior Software Engineer to join our product team. You will design, build,
and maintain scalable web applications while collaborating closely with cross-functional teams.

Requirements:
- 3+ years of professional software development experience
- Strong proficiency in Python and JavaScript/TypeScript
- Experience with web frameworks such as Django, Flask, React, or Angular
- Solid knowledge of SQL databases (PostgreSQL, MySQL) and NoSQL (MongoDB, Redis)
- Familiarity with RESTful API design and microservices architecture
- Experience with Git, CI/CD pipelines, and automated testing
- Cloud platform experience (AWS, GCP, or Azure)
- Understanding of Docker and container orchestration (Kubernetes)
- Strong problem-solving, communication, and leadership skills

Nice to Have:
- Experience with machine learning or data analysis (Pandas, Scikit-learn)
- Knowledge of system design and distributed systems
- Familiarity with Agile/Scrum methodologies
- Experience with GraphQL or gRPC

Education: Bachelor's or Master's degree in Computer Science or related field"""

    return jsonify({'jd': sample_jd})


@app.route('/api/score', methods=['POST'])
def api_score():
    """
    JSON API endpoint for programmatic access.
    Accepts: multipart form with 'resumes' files and 'job_description' text.
    Returns: JSON with full scoring breakdown.
    """
    job_description = request.form.get('job_description', '').strip()
    if not job_description:
        return jsonify({'error': 'Missing job_description'}), 400

    files = request.files.getlist('resumes')
    if not files:
        return jsonify({'error': 'No resume files uploaded'}), 400

    saved_paths = []
    for file in files:
        if file and file.filename and validate_pdf(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            saved_paths.append(filepath)

    if not saved_paths:
        return jsonify({'error': 'No valid PDF files'}), 400

    try:
        results, df, _ = process_resumes(saved_paths, job_description)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # Serialize results for JSON
    response = []
    for r in results:
        response.append({
            'rank': r['rank'],
            'name': r['name'],
            'filename': r['filename'],
            'ats_score': r['composite_score'],
            'breakdown': {
                'semantic_similarity': r['semantic_score'],
                'skill_match': r['skill_score'],
                'experience_match': r['experience_score'],
                'education_match': r['education_score'],
            },
            'matched_skills': r['skills_detail']['matched'],
            'missing_skills': r['skills_detail']['missing'],
            'experience_years': r['experience_years'],
            'education_level': r['education_level'],
        })

    return jsonify({'candidates': response, 'total': len(response)})


if __name__ == '__main__':
    # Warm up the SBERT model on startup
    print("\n" + "=" * 55)
    print("  AI-Powered ATS Resume Screening System")
    print("  Loading ML models...")
    print("=" * 55)

    try:
        from semantic_model import warmup
        warmup()
    except Exception as e:
        print(f"Warning: Could not pre-load model: {e}")
        print("Model will load on first request instead.")

    print("\n  Ready! Open http://127.0.0.1:5000 in your browser\n")
    app.run(debug=True, port=5000, use_reloader=False)
