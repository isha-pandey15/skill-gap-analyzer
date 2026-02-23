import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}
# ===============================
# AI QUERY FUNCTION
# ===============================
def query_model(prompt):
    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json={"inputs": prompt},
            timeout=30
        )

        result = response.json()

        if isinstance(result, list):
            return result[0]["generated_text"]

    except:
        pass

    return None


# ===============================
# FALLBACK SKILL DETECTOR
# ===============================
def simple_skill_extract(text):

    skills_db = [
        "python","java","c++","sql","html","css",
        "javascript","react","node","machine learning",
        "data analysis","excel","power bi","git",
        "photoshop","illustrator","seo","marketing",
        "bootstrap","django","flask","ui design"
    ]

    found = []
    text = text.lower()

    for skill in skills_db:
        if skill in text:
            found.append(skill)

    return ", ".join(found)


# ===============================
# STEP 1: EXTRACT SKILLS
# ===============================
def extract_skills(client, resume_text):

    prompt = f"Extract technical skills from resume: {resume_text}"

    ai_output = query_model(prompt)

    if ai_output:
        return ai_output

    return simple_skill_extract(resume_text)


# ===============================
# STEP 2: ANALYZE GAP
# ===============================
def analyze_gap(client, skills, job_desc):

    skill_list = [s.strip().lower() for s in skills.split(",") if s.strip()]
    jd = job_desc.lower()

    matched = []
    missing = []

    for skill in skill_list:
        if skill in jd:
            matched.append(skill)
        else:
            missing.append(skill)

    score = int((len(matched) / len(skill_list)) * 100) if skill_list else 0

    result = f"""
================ SKILL GAP ANALYSIS REPORT ================

MATCH SCORE: {score}%

------------------------------------------------------------
MATCHED SKILLS:
{", ".join(matched) if matched else "None"}

------------------------------------------------------------
MISSING SKILLS:
{", ".join(missing) if missing else "None"}

------------------------------------------------------------
RECOMMENDATIONS:

• Learn the missing skills listed above
• Build real-world projects
• Take certification courses
• Practice interview problems

============================================================
"""

    return result, score