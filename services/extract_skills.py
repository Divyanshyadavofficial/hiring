import re

SKILLS_DB = [
    "python", "java", "c++", "javascript",
    "machine learning", "deep learning", "nlp",
    "sql", "mysql", "postgresql", "mongodb",
    "docker", "kubernetes", "aws",
    "html", "css", "react", "node.js",
    "pandas", "numpy", "tensorflow", "pytorch"
]

def extract_skills(text):
    text = text.lower()
    found_skills = set()

    for skill in SKILLS_DB:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found_skills.add(skill)

    return list(found_skills)