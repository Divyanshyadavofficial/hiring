from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")

)

def generate_jd(title, skills, experience, feedback=None):

    prompt = f"""
    Generate a professional job description.

    Job Title: {title}
    Skills: {skills}
    Experience: {experience}
    """

    if feedback:
        prompt += f"""

        The previous JD was rejected.

        Recruiter feedback:
        {feedback}

        Improve the job description based on this feedback.
        """

    prompt += """

    Include:
    - Role overview
    - Responsibilities
    - Required skills
    """

    response = llm.invoke(prompt)

    return response.content

