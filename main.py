import os
import shutil
import sqlite3
import uuid
import json
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

from services.resume_parser import extract_text_from_pdf
from services.extract_skills import extract_skills
UPLOAD_FOLDER = "resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
candidates = []

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
        extracted_text = extract_text_from_pdf(file_path)
        skills = extract_skills(extracted_text)
        skills_json = json.dumps(skills)



        conn = sqlite3.connect('hiring.db')   # FIXED PATH
        cursor = conn.cursor()

        cursor.execute(
        "INSERT INTO candidates (filename, resume_text, skills) VALUES (?, ?, ?)",
        (filename, extracted_text, skills_json) 
        )
        conn.commit()
        conn.close()
        return{
            "message": "Resume uploaded successfully",
            "filename": filename
        }
    except Exception as e:
        return {"error":str(e)}

    

# ============================
# CANDIDATES API (FOR RECRUITER)
# ============================

@app.get("/candidates")
def get_candidates():
    
    conn = sqlite3.connect('hiring.db')   # FIXED PATH
    cursor = conn.cursor()

    cursor.execute(
        "SELECT filename, skills FROM candidates"
    )
    rows =  cursor.fetchall()
    conn.close()

    candidates = []
    for row in rows:
        filename = row[0]
        skills_json = row[1]

        skills = json.loads(skills_json)

        candidates.append({
            "filename": filename,
            "skills": skills
        })

    return{
        "candidates":candidates
    }


# ============================
# MATCHING ENDPOINT
# ============================
from services.matcher import skill_matcher

class MatchRequest(BaseModel):
    filename: str


@app.post("/match-resume")
async def match_resume(request:MatchRequest):
    try:
        conn = sqlite3.connect("hiring.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT resume_text FROM candidates WHERE filename = ?",
            (request.filename,)
        )
        row = cursor.fetchone()

        if not row:
            conn.close()
            return{"error":"Candidate not found"}
        resume_text = row[0]

        cursor.execute("SELECT jd_text FROM job_descriptions ORDER BY id DESC LIMIT 1")
        jd_row  = cursor.fetchone()
        conn.close()
        
        if not jd_row:
            return {"error":"No JD found"}
        jd_text = row[0]
        result = skill_matcher(jd_text,resume_text)
        return result
    except Exception as e:
        return{"error":str(e)}
    


# ============================
# RANKING ENDPOINT
# ============================
        
"""step -1 to fetch the jd text we have id as jd_text that is returned
by generate jd function we can store the jd text in the ranker algo

step - 2 for every candidatefetch the file name and resumetext from the db 


step -3 for each candidate calculate the score and return the
matched skills,missing skills,score add it to the list 

step - 4 sort these candidates by score 
step - 5 make a get endpoint that will get all the details
click the match all candidates button and it will render the
results in the ui


now what my optimized solution is that i already calculated 
the skills for each candidate and stored them in the db

so scores and matching and missing skills are calculated 
by skill matcher function in this route again if they need 
to otherwise they are calculated in the match skills endpoint 

after this step store them in a candidate list make a get endpoint
and render it in the ui after clicking the match all button
"""
@app.get("/match-all")
async def match_all():
   try: 
        conn = sqlite3.connect('hiring.db')
        cursor = conn.cursor()

        cursor.execute("SELECT jd_text " \
        "FROM job_descriptions " \
        "ORDER BY id DESC " \
        "LIMIT 1")
        row = cursor.fetchone()
        if not row:
            conn.close()
            return{"error":"jd not found"}
        jd_text = row[0]

        cursor.execute("SELECT filename, skills FROM candidates")
        candidates= cursor.fetchall()
        if not row:
            conn.close()
            return{"error":"candidates skills not found"}
        
        jd_skills = set(extract_skills(jd_text))
        candidate_results = []
        for filename, skills in candidates:
            candidate_skills = set(json.loads(skills))
            matched = jd_skills & candidate_skills
            missing = jd_skills - candidate_skills

            score = len(matched) / len(jd_skills)

            candidate_results.append({
                "filename": filename,
                "score": score,
                "matched_skills": list(matched),
                "missing_skills": list(missing)
            })
        candidate_results.sort(key =lambda x:x["score"],reverse=True)
        conn.close()
        return{"results":candidate_results}
   except Exception as e:
        return{"error":str(e)}
    
       