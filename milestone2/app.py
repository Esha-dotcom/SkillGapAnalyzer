import streamlit as st
import re
import nltk
import spacy
from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# -------------------------------
# NLP Preprocessing
# -------------------------------
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)

    tokens = text.split()

    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    doc = nlp(" ".join(tokens))
    lemmas = [token.lemma_ for token in doc]

    return lemmas


# -------------------------------
# Skill Database
# -------------------------------
SKILL_DB = [
    "python", "java", "c++", "machine learning", "deep learning",
    "data science", "data analysis", "sql", "excel", "nlp",
    "tensorflow", "pandas", "communication", "teamwork",
    "problem solving", "ai", "statistics", "power bi",
    "tableau", "cloud computing", "aws", "docker"
]


# -------------------------------
# Skill Extraction
# -------------------------------
def extract_skills(tokens, skill_db):
    text = " ".join(tokens)
    found_skills = set()

    for skill in skill_db:
        if skill in text:
            found_skills.add(skill)

    return found_skills


# -------------------------------
# Matching + Percentage
# -------------------------------
def match_skills(resume_skills, job_skills):
    matching = resume_skills.intersection(job_skills)
    missing = job_skills - resume_skills
    return matching, missing


def calculate_match_percentage(matching, job_skills):
    if len(job_skills) == 0:
        return 0
    return (len(matching) / len(job_skills)) * 100


# -------------------------------
# STREAMLIT UI
# -------------------------------
st.set_page_config(page_title="SkillGap AI", layout="centered")

st.title(" SkillGap AI")
st.write("Upload Resume and Job Description to analyze skill gap using NLP")

# Upload files
resume_file = st.file_uploader("Upload Resume (.txt)", type=["txt"])
job_file = st.file_uploader("Upload Job Description (.txt)", type=["txt"])

if st.button("Analyze"):
    if resume_file and job_file:
        resume_text = resume_file.read().decode("utf-8")
        job_text = job_file.read().decode("utf-8")

        # Preprocess
        resume_tokens = preprocess_text(resume_text)
        job_tokens = preprocess_text(job_text)

        # Extract skills
        resume_skills = extract_skills(resume_tokens, SKILL_DB)
        job_skills = extract_skills(job_tokens, SKILL_DB)

        # Match
        matching, missing = match_skills(resume_skills, job_skills)

        # Percentage
        match_percent = calculate_match_percentage(matching, job_skills)

        # Output
        st.subheader("📊 Results")

        st.write("✅ **Matching Skills:**", list(matching))
        st.write("❌ **Missing Skills:**", list(missing))

        st.progress(int(match_percent))
        st.write(f" **Match Percentage: {match_percent:.2f}%**")

    else:
        st.warning("Please upload both files!")