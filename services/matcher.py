from __future__ import annotations
from extract_skills import SKILLS_DB
import re
def skill_matcher(jd_text,resume_text):
    jd_skills_set = ()
    resume_skills_set = ()
    jd_text = jd_text.lower()
    resume_text = resume_text.lower()
    for skill in SKILLS_DB:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if(re.search(pattern,jd_text)):
            jd_skills_set.add(skill)
        if(re.search(pattern,resume_text)):
            resume_skills_set.add(skill)

    matched_skills = jd_skills_set & resume_skills_set
    if len(jd_skills_set) ==0:
        score = 0
    else: 
        score = len(matched_skills) / len(jd_skills_set)
    
    missing_skills = jd_skills_set - matched_skills
    return{
        "score":score,
        "matched_skills":matched_skills,
        "missing_skills":missing_skills
    }
    



