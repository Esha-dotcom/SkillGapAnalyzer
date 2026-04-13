import streamlit as st
import re
import spacy
import nltk
from nltk.corpus import stopwords
from io import BytesIO

# File handling
import PyPDF2
import docx

# Load NLP
nltk.download('stopwords')
nlp = spacy.load("en_core_web_sm")

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="SkillGap AI", layout="wide")

# -------------------------------
# CUSTOM CSS (PROFESSIONAL UI)
# -------------------------------
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
h1, h2, h3 {
    color: #ffffff;
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
.result-box {
    padding: 15px;
    border-radius: 10px;
    background-color: #1c1f26;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# TITLE
# -------------------------------
st.title(" SkillGap AI Analyzer")
st.write("Upload Resume & Job Description to analyze skill gap using NLP")

# -------------------------------
# FILE TEXT EXTRACTION
# -------------------------------
def extract_text(file):
    if file.name.endswith(".txt"):
        return file.read().decode("utf-8")

    elif file.name.endswith(".pdf"):
        pdf = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        return text

    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return " ".join([para.text for para in doc.paragraphs])

    return ""


# -------------------------------
# NLP PREPROCESSING
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
# SKILL DATABASE (EXPANDED)
# -------------------------------
SKILL_DB = [
    "python", "java", "c++", "machine learning", "deep learning",
    "data science", "data analysis", "sql", "excel", "nlp",
    "tensorflow", "pandas", "communication", "teamwork",
    "problem solving", "ai", "statistics", "power bi",
    "tableau", "cloud computing", "aws", "docker",
    "flask", "streamlit", "html", "css", "javascript",
    "react", "nodejs", "mongodb", "git", "linux"
]


# -------------------------------
# SKILL EXTRACTION
# -------------------------------
def extract_skills(tokens, skill_db):
    text = " ".join(tokens)
    found_skills = set()

    for skill in skill_db:
        if skill in text:
            found_skills.add(skill)

    return found_skills


# -------------------------------
# MATCHING
# -------------------------------
def match_skills(resume_skills, job_skills):
    matching = resume_skills & job_skills
    missing = job_skills - resume_skills
    return matching, missing


def calculate_match_percentage(matching, job_skills):
    if len(job_skills) == 0:
        return 0
    return (len(matching) / len(job_skills)) * 100


# -------------------------------
# UI INPUTS (ALIGNED)
# -------------------------------
col1, col2 = st.columns(2)

# Resume Section
with col1:
    st.markdown("### 📄 Resume Upload")
    resume_file = st.file_uploader(
        "Upload Resume",
        type=["txt", "pdf", "docx"],
        label_visibility="collapsed"
    )

# Job Description Section
with col2:
    st.markdown("### 💼 Job Description")
    job_file = st.file_uploader(
        "Upload Job Description",
        type=["txt", "pdf", "docx"],
        key="jd_upload",
        label_visibility="collapsed"
    )


# -------------------------------
# ANALYZE BUTTON
# -------------------------------
if st.button("🔍 Analyze Skill Gap"):

    # Normalize inputs
    has_file = job_file is not None

    # Case 1: Resume missing
    if not resume_file:
        st.warning("⚠️ Please upload a resume")

    # Case 2: NONE given
    elif not has_file:
        st.warning("⚠️ Please upload a job description")

    else:
        # ✅ VALID CASE

        # Resume
        resume_text = extract_text(resume_file)

        # Job Description
        job_text = extract_text(job_file)

        # NLP
        resume_tokens = preprocess_text(resume_text)
        job_tokens = preprocess_text(job_text)

        # Skills
        resume_skills = extract_skills(resume_tokens, SKILL_DB)
        job_skills = extract_skills(job_tokens, SKILL_DB)

        # Matching
        matching, missing = match_skills(resume_skills, job_skills)

        # Score
        match_percent = calculate_match_percentage(matching, job_skills)

        # OUTPUT
        st.subheader("📊 Analysis Results")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("### ✅ Matching Skills")
            st.write(list(matching))

        with col2:
            st.write("### ❌ Missing Skills")
            st.write(list(missing))

        with col3:
            st.write("### 🎯 Match Score")
            st.progress(int(match_percent))
            st.write(f"{match_percent:.2f}%")