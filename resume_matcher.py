from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer, util
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global model variable
model = None

def load_model():
    """Load the SentenceTransformer model."""
    global model
    try:
        if model is None:
            logger.info("Loading SentenceTransformer model...")
            model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Model loaded successfully")
        return model
    except Exception as e:
        logger.error(f"Error loading SentenceTransformer model: {e}")
        raise

# Enhanced job dataset with more diverse roles
jobs = [
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

def extract_text_from_pdf(path):
    """Extract text from a PDF file."""
    try:
        if not os.path.exists(path):
            logger.error(f"PDF file not found: {path}")
            return ""
            
        reader = PdfReader(path)
        text = ""
        
        for page_num, page in enumerate(reader.pages):
            try:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            except Exception as e:
                logger.warning(f"Error extracting text from page {page_num + 1}: {e}")
                continue
                
        return text.strip()
    except Exception as e:
        logger.error(f"Error extracting text from PDF {path}: {e}")
        return ""

def match_jobs(resume_text):
    """Match resume text to job descriptions and return the best fit and top matches."""
    try:
        if not resume_text or not resume_text.strip():
            logger.warning("Empty resume text provided")
            return "No match found", 0.0, []
            
        # Load model
        model = load_model()
        
        # Encode resume text
        resume_embedding = model.encode(resume_text)
        matches = []

        # Calculate similarity scores for each job
        for job in jobs:
            try:
                job_embedding = model.encode(job['description'])
                score = float(util.cos_sim(resume_embedding, job_embedding))
                
                # Create a copy of job dict to avoid modifying original
                job_match = job.copy()
                job_match['score'] = round(score * 100, 2)
                matches.append((score, job_match))
                
            except Exception as e:
                logger.warning(f"Error processing job {job.get('title', 'Unknown')}: {e}")
                continue

        if not matches:
            logger.warning("No job matches found")
            return "No match found", 0.0, []

        # Sort by score (descending)
        matches.sort(reverse=True, key=lambda x: x[0])
        
        # Get top 5 matches
        top_matches = [match[1] for match in matches[:5]]
        best_role = top_matches[0]['title'] if top_matches else "No match found"
        role_score = top_matches[0]['score'] if top_matches else 0.0

        logger.info(f"Best match found: {best_role} with score {role_score}%")
        
        return best_role, role_score, top_matches
        
    except Exception as e:
        logger.error(f"Error matching jobs: {e}")
        return "Error", 0.0, []

def get_job_recommendations(skills_list):
    """Get job recommendations based on a list of skills."""
    try:
        if not skills_list:
            return []
            
        model = load_model()
        skills_text = " ".join(skills_list)
        skills_embedding = model.encode(skills_text)
        
        recommendations = []
        for job in jobs:
            job_embedding = model.encode(job['description'])
            score = float(util.cos_sim(skills_embedding, job_embedding))
            
            if score > 0.3:  # Threshold for recommendations
                job_rec = job.copy()
                job_rec['score'] = round(score * 100, 2)
                recommendations.append(job_rec)
        
        # Sort by score
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:3]  # Top 3 recommendations
        
    except Exception as e:
        logger.error(f"Error getting job recommendations: {e}")
        return []