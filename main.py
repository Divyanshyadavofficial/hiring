from fastapi import FastAPI,Form,Request
from jd_generator import generate_jd
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import sqlite3
from database import create_table
create_table()

app = FastAPI()

class ApprovedJD(BaseModel):
    jd: str

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate-jd")
def create_jd(
    title: str = Form(...),
    skills: str = Form(...),
    experience: str = Form(...)
):
    jd = generate_jd(title,skills,experience)
    return {"jd":jd}


@app.post("/approve-jd")
def approve_jd(data: ApprovedJD):
    conn = sqlite3.connect('hiring.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO job_descriptions (jd_text) VALUES (?)",
        (data.jd,)
    )

    conn.commit()
    conn.close()
    return {"message":"JD saved successfully"}