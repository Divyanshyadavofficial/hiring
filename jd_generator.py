from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")

)

def generate_jd(title,skills,experience):
    prompt = f"""
    Generate a professional job description.

    Job Title:{title}
    Skills:{skills}
    Experience:{experience}

    Include: 
    - Role overview
    - Responsibilities
    - Required skills
    """
    response = llm.invoke(prompt)
    return response.content

