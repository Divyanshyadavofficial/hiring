from __future__ import annotations
from extract_skills import SKILLS_DB
import re


def skill_matcher(jd_text,resume_text):
    """
    Compare skills between a Job Description (JD) and a Resume.

    This function extracts skills from both the JD text and resume text
    using a predefined SKILLS_DB and regex pattern matching. It then
    computes how well the resume matches the JD based on skill overlap.

    Args:
        jd_text (str): The job description text containing required skills.
        resume_text (str): The candidate's resume text.

    Returns:
        dict: A dictionary containing:
            - score (float): Matching score calculated as:
                             (number of matched skills) / (number of JD skills)
            - matched_skills (list): Skills present in both JD and resume
            - missing_skills (list): Skills present in JD but missing in resume

    Notes:
        - Text is converted to lowercase for case-insensitive matching.
        - Regex word boundaries are used to avoid partial matches.
        - If no skills are found in the JD, the score defaults to 0.
    """
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
    



