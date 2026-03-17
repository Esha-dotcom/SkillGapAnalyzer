import streamlit as st
import plotly.graph_objects as go
from utils.resume_parser import extract_text
from utils.skill_extractor import extract_skills
from utils.matcher import match_skills
from utils.jobs import get_jobs
from utils.roles import ROLE_SKILLS
from utils.roadmap import generate_roadmap
from utils.youtube import YOUTUBE_RESOURCES

st.set_page_config(page_title="SkillGapAI", layout="wide")

st.title("SkillGap AI – Career Guidance System")
st.caption("Resume Analysis • Skill Gap Detection • Learning Roadmap")

st.markdown("---")

# -----------------------------
# FILE UPLOAD SECTION
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    resume_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

with col2:
    jd_file = st.file_uploader("Upload Job Description", type=["pdf", "txt", "docx"])

desired_role = st.text_input("Enter Desired Role (Example: Data Scientist)")

analyze = st.button("Analyze Resume")

# -----------------------------
# ANALYSIS
# -----------------------------

if analyze:

    if not resume_file or not jd_file or not desired_role:
        st.warning("Please upload resume, job description and enter desired role")
        st.stop()

    # Extract text
    resume_text = extract_text(resume_file)
    jd_text = extract_text(jd_file)

    # Extract skills
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    # Match skills
    match, missing, score = match_skills(resume_skills, jd_skills)

    st.markdown("---")

    # -----------------------------
    # ATS SCORE
    # -----------------------------

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("ATS Compatibility")

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": "ATS Score"},
            gauge={
                "axis": {"range": [0,100]},
                "bar": {"color": "#00C896"}
            }
        ))

        st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # RESUME SKILLS
    # -----------------------------

    with col2:

        st.subheader("Extracted Resume Skills")

        for skill in resume_skills:
            st.success(skill)

    st.markdown("---")

    # -----------------------------
    # SKILL MATCH RESULTS
    # -----------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Matching Skills")

        for skill in match:
            st.info(skill)

    with col2:

        st.subheader("Missing Skills (From JD)")

        for skill in missing:
            st.error(skill)

    st.markdown("---")

    # -----------------------------
    # JOB RECOMMENDATION
    # -----------------------------

    st.subheader("Recommended Jobs")

    jobs = get_jobs(resume_skills)

    for job in jobs:
        st.markdown(f"• **{job}**")

    st.markdown("---")

    # -----------------------------
    # ROLE SKILL GAP ANALYSIS
    # -----------------------------

    role = desired_role.strip().lower()

    if role in ROLE_SKILLS:

        role_skills = ROLE_SKILLS[role]

        missing_role = list(set(role_skills) - set(resume_skills))

        st.subheader(f"Missing Skills for {desired_role.title()}")

        for skill in missing_role:
            st.warning(skill)

        st.markdown("---")

        # -----------------------------
        # ROADMAP
        # -----------------------------

        st.subheader("Learning Roadmap")

        roadmap = generate_roadmap(missing_role)

        for i, step in enumerate(roadmap,1):
            st.markdown(f"**Step {i} – {step}**")

        st.markdown("---")

        # -----------------------------
        # YOUTUBE RESOURCES
        # -----------------------------

        st.subheader("Recommended Learning Resources")

        for skill in missing_role:

            key = skill.lower()

            if key in YOUTUBE_RESOURCES:

                video = YOUTUBE_RESOURCES[key]

                st.markdown(f"### {skill}")

                st.video(video)

    else:

        st.error("Role not found in role database")