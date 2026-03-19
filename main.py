import os
import shutil
import sqlite3

from fastapi import FastAPI, Form, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from jd_generator import generate_jd
from database import create_table

# Initialize DB
create_table()

app = FastAPI()

# Ensure resumes folder exists
UPLOAD_FOLDER = "resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Templates
templates = Jinja2Templates(directory="templates")


# ============================
# Models
# ============================
class ApprovedJD(BaseModel):
    jd: str


# ============================
# Page Routes
# ============================
@app.get("/candidate", response_class=HTMLResponse)
def candidate_page(request: Request):
    return templates.TemplateResponse("candidate.html", {"request": request})


@app.get("/recruiter", response_class=HTMLResponse)
def recruiter_page(request: Request):
    return templates.TemplateResponse("recruiter.html", {"request": request})


# ============================
# JD GENERATION
# ============================
@app.post("/generate-jd")
def create_jd(
    title: str = Form(...),
    skills: str = Form(...),
    experience: str = Form(...)
):
    jd = generate_jd(title, skills, experience)
    return {"jd": jd}


# ============================
# APPROVE JD (SAVE TO DB)
# ============================
@app.post("/approve-jd")
def approve_jd(data: ApprovedJD):
    conn = sqlite3.connect('hiring.db')   # FIXED PATH
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO job_descriptions (jd_text) VALUES (?)",
        (data.jd,)
    )

    conn.commit()
    conn.close()

    return {"message": "JD saved successfully"}


# ============================
# REVISE JD (REJECT FLOW)
# ============================
@app.post("/revise-jd")
def revise_jd(
    title: str = Form(...),
    skills: str = Form(...),
    experience: str = Form(...),
    feedback: str = Form(...)
):
    # FIX: generate_jd expects 3 args → so we merge feedback into prompt
    improved_prompt = f"""
    Generate a professional job description.

    Job Title: {title}
    Skills: {skills}
    Experience: {experience}

    Previous JD was rejected.

    Recruiter Feedback:
    {feedback}

    Improve the JD accordingly with:
    - Better clarity
    - Updated responsibilities
    - Skills aligned with feedback
    """

    # Directly call LLM via generator
    new_jd = generate_jd(title, skills, experience + " | Feedback: " + feedback)

    return {"generated_jd": new_jd}


# ============================
# FETCH SAVED JDs
# ============================
@app.get("/get-jds")
def get_jds():
    conn = sqlite3.connect("hiring.db")
    cursor = conn.cursor()

    cursor.execute("SELECT jd_text FROM job_descriptions")
    rows = cursor.fetchall()

    conn.close()

    return {"jds": [row[0] for row in rows]}


# ============================
# RESUME UPLOAD
# ============================
@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    # Validate file type
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are allowed"}

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "Resume uploaded successfully",
        "filename": file.filename
    }