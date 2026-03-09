from fastapi import FastAPI,Form
from jd_generator import generate_jd

app = FastAPI()

@app.post("/generate-jd")
def create_jd(
    title: str = Form(...),
    skills: str = Form(...),
    experience: str = Form(...)
):
    jd = generate_jd(title,skills,experience)
    return {"jd":jd}