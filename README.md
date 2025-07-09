# 💼 AI Resume Builder & Smart Job Matcher

An intelligent, dual-purpose web application that empowers users to create AI-enhanced resumes and receive personalized job role recommendations based on resume content. This solution leverages AI, NLP, and resume parsing to assist job seekers with career advancement.

---

## 📸 Demo Screenshots

> Below is a preview of how the application displays the resume analysis and job matches:

![image](https://github.com/user-attachments/assets/ec365937-0f18-4880-994d-60d6e8d6eaa5)
![image](https://github.com/user-attachments/assets/79bf3e27-9e5b-4787-a650-640f2d851892)
![image](https://github.com/user-attachments/assets/66a217f4-4445-4421-a2fa-11d81be42f7d)
![image](https://github.com/user-attachments/assets/e391f74e-3495-448f-9227-6b692f722900)
![image](https://github.com/user-attachments/assets/57d634aa-85b1-4a25-bc1b-36a71d021fd1)
![image](https://github.com/user-attachments/assets/fc854b70-51fa-4e01-9fbd-d6526157e67a)
![image](https://github.com/user-attachments/assets/e28efca9-cab1-457b-b061-1317e2919b9c)
![image](https://github.com/user-attachments/assets/2222270b-f6fe-4a27-8d9e-8af01c513b72)
![image](https://github.com/user-attachments/assets/9d2f8549-571c-4e09-8d72-c84077903b67)
![image](https://github.com/user-attachments/assets/75ee9999-373e-4fcf-995f-0caa70442e50)
![image](https://github.com/user-attachments/assets/c961fe7a-5ec6-4e44-a048-455d90e83915)
![image](https://github.com/user-attachments/assets/4a02f913-b36d-45f2-be79-f14d18be8baf)
![image](https://github.com/user-attachments/assets/fc23f992-9525-49bc-985f-ede5276c4cfb)

---

## 🚀 Features

| Feature                    | Description                                                                |
| -------------------------- | -------------------------------------------------------------------------- |
| *Resume Upload*          | Upload .pdf or .docx files securely                                    |
| *Text Extraction*        | Extracts text (mock) from uploaded resumes                                 |
| *Job Matching*           | Matches resume to pre-defined job list using keyword similarity            |
| *ATS Scoring*            | Compares resume with job description text to give a percentage match score |
| *Downloadable Resources* | Sample resume, job description template, and resume writing tips           |
| *Logging*                | Debug and error logs saved to file and console                             |
| *Error Handling*         | Custom 404 and 500 error pages with logging                                |
| *Directory Creation*     | Creates required folders dynamically if not present                        |
| *Secure File Handling*   | Renames and saves uploads safely using secure_filename()                 |

## 📝 Dynamic Resume Input Form (det.html)

Includes sections for:

- Full Name, Email, Phone  
- Career Summary / Objective (AI-enhanced)  
- Key Skills (comma-separated)  
- Work Experience (with grammar check)  
- Education, Certifications  
- Optional: Projects, Languages, Awards, Volunteering, Interests, Publications, References, Additional Info  

### 🤖 AI-Powered Enhancements

- Grammar correction and auto-formatting  
- Auto-generated summary from skills and experience  
- Smart capitalization and punctuation fixes  
- PDF Export functionality  

---

## 💳 Pricing Page Overview (premium.html + premium.css)

This section powers the **premium subscription plans** selection interface. Users can view discounted pricing, choose a plan, and securely proceed with a purchase.

## 📸 Demo Screenshots

![image](https://github.com/user-attachments/assets/06347bfd-c01d-40e8-9bcd-97a94c30e33d)
![image](https://github.com/user-attachments/assets/ec726c85-e5f9-4ff0-b352-4b70aebfef90)



## 📸 Final Outcome

![Screenshot 2025-07-09 211421](https://github.com/user-attachments/assets/6db3e327-46b6-4339-85f4-591ccf599f3e)



### 🌟 Highlights

| Highlights               | Description                                                                               |
|--------------------------|-------------------------------------------------------------------------------------------|
| *Resume Upload*          | Secure upload of .pdf or .docx resumes                                                    |
| *Text Extraction*        | Extracts resume content using mock parsing logic                                          |
| *Job Matching*           | Suggests suitable job roles using keyword-based similarity                                |
| *ATS Scoring*            | Compares resume with job descriptions and provides a match percentage                     |
| *Dynamic Resume Builder* | AI-powered input form with sections for personal, educational, and professional details   |
| *AI Enhancements*        | Grammar correction, auto-formatting, and smart summary generation                         |
| *PDF Export*               | Download the completed resume in a clean PDF format                                       |
| *Error Handling & Logging* | Custom 404/500 error pages and logs for debugging                                       |
| *Secure File Handling*     | Uses secure_filename() and creates required directories automatically                       |

---

## 💳 Premium Subscription Plans

A dedicated *pricing page* that displays subscription options with responsive design and country-specific discounts.

### 🌐 Responsive Features:

- 3 Subscription Tiers:
  - *Monthly*
  - *Quarterly* (Most Popular)
  - *Yearly* (Best Value)

---


---

## 🛠️ Tech Stack

| *Category*           | *Technology / Tool*               | *Purpose / Use*                                                           |
| ---------------------- | ----------------------------------- | --------------------------------------------------------------------------- |
| *Backend (Core)*     | Python                              | Core programming language                                                   |
|                        | Flask                               | Web framework to build routes, APIs, and handle HTTP requests               |
|                        | Jinja2                              | Templating engine to render dynamic HTML                                    |
|                        | Werkzeug                            | Secure file upload handling (secure_filename)                             |
|                        | Logging                             | Error and activity tracking (debug logs, error logs)                        |
|                        | OS, datetime (Python stdlib)        | File system operations and timestamping                                     |
| *Resume Processing*  | Mock extraction logic               | Simulated .pdf and .docx text extraction                                |
|                        | File Uploads                        | Handles PDF/DOCX uploads via form                                           |
|                        | (Option: PyPDF2, python-docx)       | For real PDF and DOCX text extraction (not yet added)                       |
| *Job Matching & ATS* | Custom similarity function          | Basic keyword matching (set intersection logic)                             |
|                        | Predefined Job List (Python)        | List of sample job descriptions for mock matching                           |
|                        | ATS Score                           | Compares resume content with job description and returns a percentage score |
| *Frontend*           | HTML5                               | Page structure and content                                                  |
|                        | CSS                                | Styling and layout                                                          |
|                        | JavaScript                         | Frontend logic/interactivity                                                |
| *File Management*    | uploads/ directory                | Stores uploaded resumes temporarily                                         |
|                        | downloads/ directory              | Stores dynamically generated files (resume samples, tips, templates)        |
|                        | templates/ directory              | Contains HTML templates (main.html, ats.html, etc.)                     |
|                        | static/ directory                 | CSS and JS files for frontend styling and behavior                          |
| *Configuration*      | DevelopmentConfig                 | Centralized config (UPLOAD\_FOLDER, LOG\_FILE, etc.)                        |
|                        | Environment Variables               | For PORT, SESSION_SECRET, and other secrets                             |
|                        | app.run(...)                      | Launches the development server                                             |
| *Optional / Future*  | PyPDF2 / python-docx                | Real text extraction from PDF/DOCX                                          |
|                        | sentence transformers | For machine learning and NLP-based job matching                             |
|                        | Flask-Login        | User authentication                                                                         |
---


## Tools Used


- *Used Pre-trained Model*        
- *Used ChatGPT to fix few errors and research* 

---


## 📁 Folder Structure

smart-job-matcher/
├── app.py                  # Main Flask app (connects everything)
├── resume_matcher.py       # NEW: Resume processing logic
├── templates/
│   ├── main.html           # Landing page
│   ├── index.html          # Job matcher interface (resume upload)
│   ├── det.html            # AI-powered resume builder
│   ├── premium.html        # Pricing and subscription plans
│             
├── static/
│   ├── main.css            # General styles
│   ├── index.css           # Styles for job matcher
│   ├── det.css             # Styles for resume builder
│   ├── premium.css         # Styles for pricing page
│   └── js/
│       └── main.js      # Resume upload handler
├── uploads/                # (auto-created if not present)
├── README.md               # Project documentation
