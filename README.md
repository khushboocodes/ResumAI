# 💼 Smart Job Matcher

**Smart Job Matcher** is an AI-powered web application that allows users to upload their resumes (PDF only) and receive the best-fit job role along with top matching job listings. It leverages resume parsing and intelligent matching logic to guide users toward the most suitable career opportunities.

---

## 📸 Demo Screenshots

> Below is a preview of how the application displays the resume analysis and job matches:

![image1](https://github.com/user-attachments/assets/c961fe7a-5ec6-4e44-a048-455d90e83915)
![image2](https://github.com/user-attachments/assets/4a02f913-b36d-45f2-be79-f14d18be8baf)
![image3](https://github.com/user-attachments/assets/fc23f992-9525-49bc-985f-ede5276c4cfb)

---

## 🚀 Features

- 📄 **Resume Upload & Parsing**  
  Upload a resume (PDF) and extract structured details like name, skills, education, and experience.

- 🔍 **AI-Based Role Suggestion**  
  Recommends the most relevant job role using intelligent analysis.

- 🎯 **Top Job Match Recommendations**  
  Lists best-matching job titles with descriptions, company names, and matching scores.

- 🧠 **Keyword Optimization**  
  Helps optimize resumes to be ATS-friendly using keyword suggestions.

- 🌐 **Multilingual Interface Ready**  
  Easily extendable to support multiple languages.

- 🔒 **Data Privacy & Security**  
  Resume data is processed temporarily and never stored permanently.

---

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

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **HTML, CSS, JS** | Frontend interface and interactivity |
| **Font Awesome** | Icons and visual enhancements |
| **html2pdf.js** | Exporting resumes to PDF |
| **Python (Flask)** | Backend resume processing and job matching |
| **PyPDF2 / NLP tools** | Resume parsing and keyword analysis |

---

## 📁 Folder Structure

smart-job-matcher/
├── index.html 
├── index.css 
├── det.html # Resume builder with AI features
├── det.css # Styles for resume builder
└── README.md # Project documentation (this file)
