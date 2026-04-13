import PyPDF2
import docx2txt
import re
import pandas as pd
from skill_database import ROLE_SKILLS

def clean_text(text):
    # Remove special characters and extra whitespace
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text.lower()

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return clean_text(text)

def extract_text_from_docx(file):
    text = docx2txt.process(file)
    return clean_text(text)

def extract_skills(text):
    # Consolidate all skills from our database
    all_possible_skills = set()
    for skills in ROLE_SKILLS.values():
        all_possible_skills.update(skills)
    
    extracted = []
    # Work with cleaned text which is already lowercase
    for skill in all_possible_skills:
        # Simple regex to find skills as whole words
        # Note: clean_text removes hyphens, so we should too in our match list
        skill_pattern = skill.lower().replace("-", " ").replace(".", "")
        pattern = r'\b' + re.escape(skill_pattern) + r'\b'
        if re.search(pattern, text):
            extracted.append(skill)
    return list(set(extracted))

def calculate_ats_score(resume_skills, jd_skills):
    if not jd_skills:
        return 0
    match_count = len(set(resume_skills) & set(jd_skills))
    score = (match_count / len(jd_skills)) * 100
    return round(score, 2)

def identify_missing_skills(resume_skills, required_skills):
    missing = [skill for skill in required_skills if skill not in resume_skills]
    return missing

def get_job_recommendations(skills):
    # In a real app, this would call an API like SerpApi or Scraper
    # Mocking recommendations based on skill intersection
    recommendations = []
    
    for role, role_skills in ROLE_SKILLS.items():
        match_count = len(set(skills) & set(role_skills))
        if match_count >= 2:
            recommendations.append(role)
            
    return recommendations[:3] # Top 3
