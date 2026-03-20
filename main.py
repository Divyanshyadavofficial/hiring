import os
import shutil
import sqlite3
import uuid

from fastapi import FastAPI, Form, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from jd_generator import generate_jd
from database import create_table

# Initialize DB
create_table()

app = FastAPI()



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

UPLOAD_FOLDER = "resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith(".pdf"):
            return {"error":"Only PDF files are allowed"}
        
        contents = await file.read()
        if len(contents)>2*1024 *1024:
            return {"error":"File size exceeds 2MB limit"}
        
        unique_id = str(uuid.uuid4())
        filename = f"{unique_id}.pdf"
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        with open(file_path,"wb") as buffer:
            buffer.write(contents)
        return {
            "message":"Resume uploaded successfully",
            "filename":filename
        }
    except Exception as e:
        return {"error": str(e)}