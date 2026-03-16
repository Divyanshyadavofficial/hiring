# AI Automated Hiring System

An AI-powered recruitment assistant that automates the early stages of the hiring process.  
This system helps recruiters generate job descriptions, review them with feedback, upload resumes, parse candidate information, and prepare data for intelligent candidate matching.

The project demonstrates a **Human-in-the-Loop AI system** where AI generates outputs and recruiters refine them through feedback.

---

# Project Overview

Recruitment teams spend significant time writing job descriptions and reviewing resumes.  
This project reduces that effort by introducing AI-powered automation.

The system currently supports:

- AI Job Description Generation
- Human-in-the-Loop JD Revision
- Job Description Approval & Storage
- Resume Upload
- Resume Text Extraction
- AI Resume Parsing

Future versions will include **AI candidate matching and ranking**.

---

# System Architecture

```
Recruiter
   │
   ▼
AI Job Description Generator
   │
   ▼
Human Review (Approve / Reject)
   │
   ▼
Regeneration using Feedback
   │
   ▼
Approved JD Database
   │
   ▼
Resume Upload
   │
   ▼
Resume Text Extraction
   │
   ▼
AI Resume Parsing
   │
   ▼
Candidate Database
   │
   ▼
JD ↔ Resume Matching (Future)
   │
   ▼
Candidate Ranking
```

---

# Features

## 1. AI Job Description Generator

Recruiters can generate a professional job description by entering:

- Job title
- Required skills
- Experience level

The system uses a Large Language Model (LLM) to generate structured job descriptions including:

- Role overview
- Responsibilities
- Required skills

---

## 2. Human-in-the-Loop JD Revision

Recruiters can review the generated JD and choose to:

- Approve the job description
- Reject and provide feedback

If rejected, the system regenerates an improved job description using the recruiter’s feedback.

This creates an **AI feedback loop** that improves output quality.

---

## 3. Job Description Approval

Approved job descriptions are stored in a **SQLite database**, allowing the system to maintain a repository of finalized job roles.

---

## 4. Resume Upload

Recruiters can upload candidate resumes in **PDF format**.

Uploaded resumes are saved locally in the system for further processing.

---

## 5. Resume Text Extraction

The system extracts text from uploaded resumes using a PDF parsing library.

This converts the resume into machine-readable text.

---

## 6. AI Resume Parsing

The extracted resume text is processed by a Large Language Model to extract structured candidate information such as:

- Name
- Skills
- Experience
- Education

This allows automated candidate analysis.

---

# Technology Stack

## Backend
- Python
- FastAPI

## AI Model
- LLM via Groq API

## Database
- SQLite

## Resume Processing
- pdfplumber

## Frontend
- HTML
- CSS
- JavaScript (Fetch API)

---

# Project Structure

```
ai-hiring-system/

main.py
jd_generator.py
resume_parser.py
database.py

templates/
    index.html

resumes/

hiring.db
README.md
```

---

# Workflow

## Job Description Generation

1. Recruiter enters job title, skills, and experience.
2. AI generates a job description.
3. Recruiter reviews the output.

---

## JD Revision Flow

1. Recruiter rejects the JD.
2. Recruiter provides feedback.
3. AI regenerates the JD using feedback.
4. Recruiter approves the final JD.

---

## Resume Processing Flow

1. Recruiter uploads a resume.
2. System extracts resume text.
3. AI parses the resume.
4. Structured candidate information is generated.

---

# Example Output

## Generated Job Description

```
Role: Backend Engineer

Responsibilities:
- Build scalable backend services
- Develop APIs using FastAPI
- Collaborate with frontend teams

Required Skills:
- Python
- FastAPI
- Docker
```

---

## Parsed Resume

```
Name: John Doe
Skills: Python, FastAPI, Docker
Experience: 3 years
Education: B.Tech Computer Science
```

---

# Future Improvements

The next stages of development include:

### Candidate Matching
Match resumes with job descriptions using embeddings.

### Candidate Ranking
Rank candidates based on skills, experience, and similarity to job requirements.

### Vector Database Integration
Store resume and JD embeddings for efficient semantic search.

### Recruiter Dashboard
Display approved job descriptions and candidate matches.

### AI Explanation Layer
Explain why a candidate matches a job using Retrieval Augmented Generation (RAG).

---

# Installation

Clone the repository:

```
git clone https://github.com/yourusername/ai-hiring-system.git
cd ai-hiring-system
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the application:

```
uvicorn main:app --reload
```

Open in browser:

```
http://127.0.0.1:8000
```

---

# Purpose of the Project

This project demonstrates how AI can assist recruitment workflows by automating repetitive tasks while allowing recruiters to maintain control through feedback and approvals.

It showcases practical applications of:

- Large Language Models
- Human-in-the-loop AI systems
- Resume parsing automation
- Backend AI service development

---

# Author

Divyansh Yadav

---

# License

This project is open-source and available for educational purposes.