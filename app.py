from flask import Flask, request, render_template, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import re
import docx2txt
from PyPDF2 import PdfReader
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB limit
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

ALLOWED_EXTENSIONS = {'pdf', 'docx'}

# Sample job data for matching
SAMPLE_JOBS = [
    {
        "title": "Senior Software Engineer",
        "company": "TechCorp Inc.",
        "location": "San Francisco, CA",
        "description": "We are looking for a senior software engineer with experience in Python, JavaScript, React, and cloud technologies.",
        "keywords": ["python", "javascript", "react", "cloud", "aws", "docker", "kubernetes", "api", "database", "git"],
        "url": "https://example.com/job1"
    },
    {
        "title": "Data Scientist",
        "company": "DataTech Solutions",
        "location": "New York, NY",
        "description": "Seeking a data scientist with expertise in machine learning, Python, SQL, and statistical analysis.",
        "keywords": ["python", "machine learning", "sql", "tensorflow", "pandas", "statistics", "data", "analysis", "visualization", "numpy"],
        "url": "https://example.com/job2"
    },
    {
        "title": "Frontend Developer",
        "company": "WebDesign Pro",
        "location": "Austin, TX",
        "description": "Frontend developer needed with strong skills in React, TypeScript, CSS, and modern web development practices.",
        "keywords": ["react", "typescript", "css", "html", "javascript", "responsive", "ui", "ux", "webpack", "sass"],
        "url": "https://example.com/job3"
    },
    {
        "title": "DevOps Engineer",
        "company": "CloudFirst Technologies",
        "location": "Seattle, WA",
        "description": "DevOps engineer with experience in AWS, Docker, Kubernetes, CI/CD pipelines, and infrastructure automation.",
        "keywords": ["aws", "docker", "kubernetes", "ci/cd", "linux", "terraform", "jenkins", "monitoring", "automation", "scripting"],
        "url": "https://example.com/job4"
    },
    {
        "title": "Product Manager",
        "company": "Innovation Labs",
        "location": "Boston, MA",
        "description": "Product manager to lead product strategy, roadmap planning, and cross-functional team coordination.",
        "keywords": ["product management", "strategy", "roadmap", "agile", "scrum", "user research", "analytics", "stakeholder", "leadership", "planning"],
        "url": "https://example.com/job5"
    }
]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_path):
    try:
        with open(file_path, "rb") as f:
            reader = PdfReader(f)
            return "".join(page.extract_text() or "" for page in reader.pages)
    except Exception as e:
        logger.error(f"Error extracting text from PDF {file_path}: {e}")
        return ""

def extract_text(file_path):
    try:
        if file_path.endswith(".pdf"):
            return extract_text_from_pdf(file_path)
        elif file_path.endswith(".docx"):
            return docx2txt.process(file_path)
        return ""
    except Exception as e:
        logger.error(f"Error extracting text from {file_path}: {e}")
        return ""

def calculate_score(resume_text, job_keywords):
    try:
        resume_words = set(re.findall(r'\w+', resume_text.lower()))
        job_words = set(job_keywords)
        matched = resume_words & job_words
        return round((len(matched) / len(job_words)) * 100, 2) if job_words else 0
    except Exception as e:
        logger.error(f"Error calculating score: {e}")
        return 0

def match_jobs(resume_text):
    try:
        job_matches = []
        for job in SAMPLE_JOBS:
            score = calculate_score(resume_text, job["keywords"])
            job_matches.append({ **job, "score": score })
        job_matches.sort(key=lambda x: x["score"], reverse=True)
        best_role = job_matches[0]["title"] if job_matches else "General"
        role_score = job_matches[0]["score"] if job_matches else 0
        return best_role, role_score, job_matches[:5]
    except Exception as e:
        logger.error(f"Error matching jobs: {e}")
        return "General", 0, []

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/det')
def det():
    return render_template('det.html')

@app.route('/ats')
def ats():
    return render_template('ats.html')

@app.route('/premium')
def premium():
    return render_template('premium.html')

@app.route('/match', methods=['POST'])
def match():
    if 'resumeFile' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['resumeFile']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file format. Upload PDF or DOCX.'}), 400

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}")
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(filepath)

        resume_text = extract_text(filepath)
        if not resume_text:
            return jsonify({'error': 'Could not extract text from resume'}), 400

        best_role, role_score, job_matches = match_jobs(resume_text)

        return jsonify({
            'best_role': best_role,
            'role_score': role_score,
            'matches': job_matches
        })
    except Exception as e:
        logger.error(f"Error processing resume: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception as e:
                logger.warning(f"Failed to remove uploaded file: {e}")

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('templates', exist_ok=True)

    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)