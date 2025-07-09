from flask import Flask, request, render_template, jsonify, send_from_directory, send_file, make_response
from werkzeug.utils import secure_filename
import os
import logging
from datetime import datetime
from config import DevelopmentConfig

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(DevelopmentConfig.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key-for-dev")
app.config.from_object(DevelopmentConfig)

# Mock AI functionality for now
def mock_similarity_score(text1, text2):
    """Mock similarity calculation based on keyword matching"""
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    return len(intersection) / len(union) if union else 0.0

# Sample job data
JOBS = [
    {
        'title': 'Software Engineer',
        'description': 'Develop web applications using Python, Django, Flask, JavaScript, React, and REST APIs. Experience with databases, version control, and agile methodologies required.',
        'company': 'TechCorp',
        'location': 'Remote',
        'url': 'https://example.com/jobs/1'
    },
    {
        'title': 'Data Analyst',
        'description': 'Work with Excel, SQL, Python, Tableau, and Power BI to derive insights from data. Statistical analysis, data visualization, and reporting skills essential.',
        'company': 'DataLab',
        'location': 'Bangalore',
        'url': 'https://example.com/jobs/2'
    },
    {
        'title': 'Frontend Developer',
        'description': 'Build responsive web interfaces with HTML, CSS, JavaScript, React, Vue.js, and modern frontend frameworks. UI/UX design experience preferred.',
        'company': 'Webify',
        'location': 'Delhi',
        'url': 'https://example.com/jobs/3'
    },
    {
        'title': 'Data Scientist',
        'description': 'Machine learning, deep learning, Python, R, TensorFlow, PyTorch, statistical modeling, and predictive analytics. PhD or Masters preferred.',
        'company': 'AI Innovations',
        'location': 'Mumbai',
        'url': 'https://example.com/jobs/4'
    },
    {
        'title': 'DevOps Engineer',
        'description': 'AWS, Docker, Kubernetes, CI/CD pipelines, infrastructure automation, monitoring, and cloud deployment. Linux and scripting skills required.',
        'company': 'CloudTech',
        'location': 'Hyderabad',
        'url': 'https://example.com/jobs/5'
    },
    {
        'title': 'Product Manager',
        'description': 'Product strategy, roadmap planning, stakeholder management, agile methodologies, user research, and market analysis. MBA preferred.',
        'company': 'ProductCo',
        'location': 'Pune',
        'url': 'https://example.com/jobs/6'
    },
    {
        'title': 'Backend Developer',
        'description': 'Node.js, Python, Java, microservices, database design, API development, and server-side programming. Cloud experience preferred.',
        'company': 'ServerSide Inc',
        'location': 'Chennai',
        'url': 'https://example.com/jobs/7'
    },
    {
        'title': 'Mobile Developer',
        'description': 'iOS and Android development, Swift, Kotlin, React Native, Flutter, mobile UI/UX, and app store deployment experience.',
        'company': 'MobileFirst',
        'location': 'Gurgaon',
        'url': 'https://example.com/jobs/8'
    }
]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_text_from_pdf(file_path):
    """Mock PDF text extraction"""
    try:
        # For now, return placeholder text since we don't have PyPDF2
        return "Sample resume text with skills in Python, JavaScript, web development, and project management. Experience in software engineering and team leadership."
    except Exception as e:
        logger.error(f"PDF extraction error: {e}")
        return ""

def extract_text_from_docx(file_path):
    """Mock DOCX text extraction"""
    try:
        # For now, return placeholder text since we don't have python-docx
        return "Sample resume text with skills in Python, JavaScript, web development, and project management. Experience in software engineering and team leadership."
    except Exception as e:
        logger.error(f"DOCX extraction error: {e}")
        return ""

def extract_text(file_path):
    """Extract text from uploaded file"""
    try:
        if file_path.lower().endswith(".pdf"):
            return extract_text_from_pdf(file_path)
        elif file_path.lower().endswith(".docx"):
            return extract_text_from_docx(file_path)
        return ""
    except Exception as e:
        logger.error(f"Text extraction error: {e}")
        return ""

def match_jobs(resume_text):
    """Match resume to jobs using simple keyword matching"""
    try:
        if not resume_text.strip():
            return "No match found", 0.0, []

        matches = []
        
        for job in JOBS:
            try:
                # Use simple keyword matching instead of AI
                score = mock_similarity_score(resume_text, job['description'])
                job_match = job.copy()
                job_match['score'] = round(score * 100, 2)
                matches.append((score, job_match))
            except Exception as e:
                logger.warning(f"Error matching job '{job['title']}': {e}")

        if not matches:
            return "No match found", 0.0, []

        matches.sort(reverse=True, key=lambda x: x[0])
        top_matches = [match[1] for match in matches[:5]]
        best_role = top_matches[0]['title']
        role_score = top_matches[0]['score']

        return best_role, role_score, top_matches
    except Exception as e:
        logger.error(f"Job matching error: {e}")
        return "Error occurred", 0.0, []

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

    filepath = None
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
        logger.error(f"Resume processing error: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        if filepath and os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception as e:
                logger.warning(f"Failed to remove file {filepath}: {e}")

@app.route('/score', methods=['POST'])
def score():
    """ATS Score endpoint"""
    if 'resume' not in request.files or 'jobdesc' not in request.form:
        return render_template('ats.html', error='Missing resume file or job description')

    file = request.files['resume']
    job_desc = request.form['jobdesc']

    if file.filename == '' or not allowed_file(file.filename):
        return render_template('ats.html', error='Invalid file format. Upload PDF or DOCX.')

    filepath = None
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}")
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(filepath)

        resume_text = extract_text(filepath)
        if not resume_text:
            return render_template('ats.html', error='Could not extract text from resume')

        # Calculate ATS score using simple keyword matching
        score = mock_similarity_score(resume_text, job_desc)
        ats_score = round(score * 100, 2)

        return render_template('ats.html', score=ats_score)
    except Exception as e:
        logger.error(f"ATS scoring error: {e}")
        return render_template('ats.html', error='Failed to calculate ATS score')
    finally:
        if filepath and os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception as e:
                logger.warning(f"Failed to remove file {filepath}: {e}")

@app.route('/download/<file_type>')
def download_file(file_type):
    """Download files based on type"""
    try:
        if file_type == 'sample_resume':
            # Create a sample resume file
            sample_content = """JOHN DOE
johndoe@email.com | (555) 123-4567 | linkedin.com/in/johndoe

PROFESSIONAL SUMMARY
Experienced software engineer with 5+ years of expertise in full-stack development, 
specializing in Python, JavaScript, and cloud technologies. Proven track record of 
delivering scalable web applications and leading cross-functional teams.

TECHNICAL SKILLS
• Programming Languages: Python, JavaScript, Java, SQL
• Frameworks: Flask, Django, React, Node.js
• Cloud Platforms: AWS, Google Cloud, Azure
• Databases: PostgreSQL, MySQL, MongoDB
• Tools: Git, Docker, Kubernetes, CI/CD

PROFESSIONAL EXPERIENCE
Senior Software Engineer | TechCorp | 2021 - Present
• Developed and maintained 10+ web applications using Python and React
• Led a team of 5 developers in agile development processes
• Improved application performance by 40% through optimization
• Implemented CI/CD pipelines reducing deployment time by 60%

Software Engineer | StartupXYZ | 2019 - 2021
• Built RESTful APIs serving 100K+ daily requests
• Collaborated with product team to deliver user-focused features
• Mentored junior developers and conducted code reviews

EDUCATION
Bachelor of Science in Computer Science | State University | 2019
• Relevant Coursework: Data Structures, Algorithms, Software Engineering
• GPA: 3.8/4.0

PROJECTS
• E-commerce Platform: Full-stack web application with payment integration
• Data Analytics Dashboard: Real-time analytics using Python and D3.js
• Mobile App: React Native app with 10K+ downloads

CERTIFICATIONS
• AWS Certified Solutions Architect
• Google Cloud Professional Developer
"""
            
            # Create downloads directory if it doesn't exist
            downloads_dir = os.path.join(app.root_path, 'downloads')
            os.makedirs(downloads_dir, exist_ok=True)
            
            # Save sample resume
            file_path = os.path.join(downloads_dir, 'sample_resume.txt')
            with open(file_path, 'w') as f:
                f.write(sample_content)
            
            return send_file(file_path, as_attachment=True, download_name='sample_resume.txt')
            
        elif file_type == 'job_description_template':
            # Create a job description template
            job_template = """JOB TITLE: [Position Name]
COMPANY: [Company Name]
LOCATION: [City, State/Country]
EMPLOYMENT TYPE: [Full-time/Part-time/Contract]

JOB DESCRIPTION:
[Brief overview of the role and its importance to the company]

KEY RESPONSIBILITIES:
• [Responsibility 1]
• [Responsibility 2]
• [Responsibility 3]
• [Responsibility 4]
• [Responsibility 5]

REQUIRED QUALIFICATIONS:
• [Education requirement]
• [Years of experience required]
• [Technical skills needed]
• [Industry experience]
• [Certifications if any]

PREFERRED QUALIFICATIONS:
• [Additional skills that would be beneficial]
• [Nice-to-have experience]
• [Bonus qualifications]

TECHNICAL SKILLS:
• [Programming languages]
• [Frameworks and tools]
• [Software and platforms]
• [Database knowledge]

SOFT SKILLS:
• [Communication skills]
• [Leadership abilities]
• [Problem-solving skills]
• [Teamwork capabilities]

BENEFITS:
• [Salary range]
• [Health insurance]
• [Retirement plans]
• [Paid time off]
• [Other benefits]

APPLICATION PROCESS:
[Instructions on how to apply]

COMPANY CULTURE:
[Brief description of company values and work environment]
"""
            
            downloads_dir = os.path.join(app.root_path, 'downloads')
            os.makedirs(downloads_dir, exist_ok=True)
            
            file_path = os.path.join(downloads_dir, 'job_description_template.txt')
            with open(file_path, 'w') as f:
                f.write(job_template)
            
            return send_file(file_path, as_attachment=True, download_name='job_description_template.txt')
            
        elif file_type == 'resume_tips':
            # Create resume tips guide
            tips_content = """RESUME WRITING TIPS & BEST PRACTICES

1. FORMATTING GUIDELINES
• Use a clean, professional font (Arial, Calibri, or Times New Roman)
• Keep font size between 10-12 points
• Use consistent formatting throughout
• Save as PDF to maintain formatting
• Keep resume to 1-2 pages maximum

2. HEADER SECTION
• Include full name, phone number, email, and LinkedIn profile
• Use a professional email address
• Consider adding your city and state
• Make sure contact information is current

3. PROFESSIONAL SUMMARY
• Write a compelling 2-3 sentence summary
• Highlight your most relevant experience
• Include key achievements and skills
• Tailor to each job application

4. WORK EXPERIENCE
• List experiences in reverse chronological order
• Use action verbs to start each bullet point
• Quantify achievements with numbers and percentages
• Focus on accomplishments, not just duties
• Include relevant keywords from job descriptions

5. SKILLS SECTION
• List technical skills relevant to the position
• Include programming languages, software, and tools
• Mention certifications and specialized knowledge
• Keep skills current and accurate

6. EDUCATION
• Include degree type, institution, and graduation year
• Add relevant coursework if you're a recent graduate
• Include GPA if it's above 3.5
• List academic honors and achievements

7. ATS OPTIMIZATION
• Use standard section headings
• Include relevant keywords from job descriptions
• Avoid images, graphics, and complex formatting
• Use bullet points instead of paragraphs
• Save in both PDF and Word formats

8. COMMON MISTAKES TO AVOID
• Spelling and grammar errors
• Inconsistent formatting
• Including irrelevant information
• Using unprofessional email addresses
• Making it too long or too short
• Including personal information (age, photo, etc.)

9. PROOFREADING CHECKLIST
• Check for spelling and grammar errors
• Verify contact information is correct
• Ensure dates are accurate
• Review formatting consistency
• Ask someone else to review it

10. CUSTOMIZATION TIPS
• Tailor resume for each job application
• Research company and role requirements
• Adjust keywords and skills accordingly
• Highlight most relevant experiences
• Update professional summary for each application

Remember: Your resume is your first impression. Make it count!
"""
            
            downloads_dir = os.path.join(app.root_path, 'downloads')
            os.makedirs(downloads_dir, exist_ok=True)
            
            file_path = os.path.join(downloads_dir, 'resume_tips.txt')
            with open(file_path, 'w') as f:
                f.write(tips_content)
            
            return send_file(file_path, as_attachment=True, download_name='resume_writing_tips.txt')
            
        else:
            return jsonify({'error': 'Invalid file type'}), 400
            
    except Exception as e:
        logger.error(f"Download error: {e}")
        return jsonify({'error': 'File download failed'}), 500

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.errorhandler(404)
def not_found(error):
    return render_template('main.html'), 404

@app.errorhandler(500)
def server_error(error):
    logger.error(f"Server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)

    port = int(os.environ.get('PORT', 5000))
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=port)
