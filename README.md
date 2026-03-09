# AI hiring system

An AI-powered system that performs professional job hirings based on a job title, required skills, and experience level. Users can review the generated job description and approve it to store it in a database.

---

## Features

- Generate job descriptions using an LLM
- Simple web interface to input job details
- Review generated job description before approval
- Save approved job descriptions to a database
- Lightweight backend with a local database

---

## Tech Stack

- Backend: Python (FastAPI)
- Frontend: HTML, CSS, JavaScript
- AI Model: Groq Llama via LangChain
- Database: SQLite
- Template Engine: Jinja2

---

## Project Structure
JDComponent/
│
├── main.py              # FastAPI application
├── jd_generator.py      # JD generation logic
├── database.py          # Database setup
├── hiring.db            # SQLite database (auto-created)
│
├── templates/
│   └── index.html       # Frontend UI
│
└── README.md
---

## Installation

### 1. Clone the Repository
### 2. Create a Virtual Environment

Mac / Linux
python -m venv venv
source venv/bin/activate
Windows
python -m venv venv
venv\Scripts\activate

### 3. Install Dependencies

pip install fastapi uvicorn langchain-groq python-dotenv jinja2

---

## Environment Variables

Create a `.env` file in the root directory.
GROQ_API_KEY=your_groq_api_key_here
---

## Run the Application

Start the FastAPI server:uvicorn main:app –reload
