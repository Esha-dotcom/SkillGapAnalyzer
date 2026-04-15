import streamlit as st
import pandas as pd
from skill_database import ROLE_SKILLS, SKILL_ROADMAPS, YOUTUBE_RESOURCES, JOB_LOCATIONS
from utils import (
    extract_text_from_pdf, 
    extract_text_from_docx, 
    extract_skills, 
    calculate_ats_score, 
    identify_missing_skills,
    get_job_recommendations
)
import plotly.express as px
import random

# Page Configuration
st.set_page_config(
    page_title="SkillGapAI - Executive Analysis Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Premium Professional Look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Global Body Overrides */
    .stApp {
        background: linear-gradient(145deg, #0f172a 0%, #1e293b 100%);
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }

    /* Container Borders & Backgrounds */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: rgba(30, 41, 59, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        backdrop-filter: blur(12px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }

    /* Typography */
    h1 {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.025em !important;
        background: linear-gradient(to right, #60a5fa, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem !important;
    }

    h2, h3 {
        font-weight: 700 !important;
        color: #f8fafc !important;
        letter-spacing: -0.01em;
    }

    .stCaption {
        color: #94a3b8 !important;
        font-size: 1rem !important;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 14px 28px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 14px 0 rgba(59, 130, 246, 0.3) !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }

    .stButton>button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%) !important;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        color: #60a5fa !important;
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Badges/Skills */
    .missing-skill {
        background: rgba(239, 68, 68, 0.1);
        color: #f87171;
        padding: 6px 14px;
        border-radius: 9999px;
        display: inline-block;
        margin: 4px;
        border: 1px solid rgba(239, 68, 68, 0.2);
        font-size: 0.8rem;
        font-weight: 600;
    }

    .match-skill {
        background: rgba(16, 185, 129, 0.1);
        color: #34d399;
        padding: 6px 14px;
        border-radius: 9999px;
        display: inline-block;
        margin: 4px;
        border: 1px solid rgba(16, 185, 129, 0.2);
        font-size: 0.8rem;
        font-weight: 600;
    }

    /* Learning Cards */
    .yt-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 16px;
        transition: transform 0.2s ease;
    }

    .yt-card:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: #3b82f6;
    }

    .yt-skill-name {
        color: #e2e8f0;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 12px;
    }

    .yt-link-btn {
        display: inline-flex;
        align-items: center;
        background: rgba(59, 130, 246, 0.1);
        color: #60a5fa !important;
        text-decoration: none !important;
        padding: 8px 18px;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 700;
        border: 1px solid rgba(59, 130, 246, 0.2);
        transition: all 0.2s ease;
    }

    .yt-link-btn:hover {
        background: #3b82f6 !important;
        color: white !important;
    }

    /* Roadmap Steps */
    .roadmap-step {
        border-left: 3px solid #3b82f6;
        padding-left: 20px;
        margin-bottom: 24px;
    }

    .roadmap-step-title {
        color: #f1f5f9;
        font-weight: 700;
        font-size: 1.1rem;
        margin-bottom: 6px;
    }

    .roadmap-step-desc {
        color: #94a3b8;
        font-size: 0.95rem;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# Main Header
st.title("SkillGapAI")
st.caption("Precision Career Analysis and Roadmap Generation")

# Upload and Configuration Section
with st.container(border=True):
    col_u1, col_u2 = st.columns([1, 1])
    
    with col_u1:
        resume_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])
    
    with col_u2:
        jd_file = st.file_uploader("Upload Job Description (Optional)", type=["pdf", "docx", "txt"])
    
    st.markdown("---")
    col_c1, col_c2 = st.columns([2, 1])
    with col_c1:
        desired_role = st.selectbox("Select Target Role", list(ROLE_SKILLS.keys()))
    with col_c2:
        st.markdown("<div style='padding-top: 28px;'></div>", unsafe_allow_html=True)
        analyze_btn = st.button("ANALYZE PROFILE")

if analyze_btn:
    if resume_file:
        with st.spinner("Analyzing your profile..."):
            # 1. Text Extraction
            if resume_file.name.endswith(".pdf"):
                resume_text = extract_text_from_pdf(resume_file)
            else:
                resume_text = extract_text_from_docx(resume_file)
            
            jd_text = ""
            if jd_file:
                if jd_file.name.endswith(".pdf"):
                    jd_text = extract_text_from_pdf(jd_file)
                elif jd_file.name.endswith(".docx"):
                    jd_text = extract_text_from_docx(jd_file)
                else:
                    jd_text = jd_file.read().decode("utf-8")
            
            # 2. Skill Extraction
            resume_skills = extract_skills(resume_text)
            jd_skills = extract_skills(jd_text) if jd_text else ROLE_SKILLS[desired_role]
            role_required_skills = ROLE_SKILLS[desired_role]
            
            # 3. Calculation
            ats_score = calculate_ats_score(resume_skills, jd_skills)
            missing_for_jd = identify_missing_skills(resume_skills, jd_skills)
            missing_for_role = identify_missing_skills(resume_skills, role_required_skills)
            
            # --- Results Display ---
            st.markdown("---")
            
            # Metric Row
            st.subheader("Executive Summary")
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.metric("ATS MATCH RATING", f"{ats_score}%")
            with col_m2:
                st.metric("CORE COMPETENCIES", len(resume_skills))
            with col_m3:
                st.metric("IDENTIFIED GAPS", len(missing_for_role))
            
            # Progress Bar for ATS
            st.progress(ats_score/100)
            
            # Phase 2: Profile Analysis (Comparison)
            with st.container(border=True):
                st.subheader("Profile Analysis")
                col_p1, col_p2 = st.columns([1, 1])
                
                with col_p1:
                    st.write("**Identified Skills**")
                    if resume_skills:
                        for s in resume_skills:
                            st.markdown(f'<span class="match-skill">{s}</span>', unsafe_allow_html=True)
                    else:
                        st.warning("No skills detected.")
                
                with col_p2:
                    st.write(f"**Missing Skills for {desired_role}**")
                    if missing_for_role:
                        for s in missing_for_role:
                            st.markdown(f'<span class="missing-skill">{s}</span>', unsafe_allow_html=True)
                    else:
                        st.success("Core competencies matched.")

            # Phase 3: Strategic Roadmap
            with st.container(border=True):
                st.subheader(f"{desired_role} Roadmap")
                if not missing_for_role:
                    st.info("No gaps detected. Focus on project portfolio enhancement.")
                else:
                    for i, skill in enumerate(missing_for_role):
                        roadmap_text = SKILL_ROADMAPS.get(skill, f"Phase 1: Fundamental {skill} -> Phase 2: Applied Projects")
                        st.markdown(f"""
                        <div class="roadmap-step">
                            <div class="roadmap-step-title">Step {i+1}: {skill} Specialization</div>
                            <div class="roadmap-step-desc">{roadmap_text}</div>
                        </div>
                        """, unsafe_allow_html=True)

            # Phase 4: Learning Resources
            with st.container(border=True):
                st.subheader("Learning Resources")
                for skill in missing_for_role:
                    yt_link = YOUTUBE_RESOURCES.get(skill, f"https://www.youtube.com/results?search_query={skill}+tutorial")
                    st.markdown(f"""
                    <div class="yt-card">
                        <div class="yt-skill-name">{skill}</div>
                        <a href="{yt_link}" class="yt-link-btn" target="_blank">Watch Tutorial</a>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Phase 5: Market Opportunities
            with st.container(border=True):
                st.subheader("Market Opportunities")
                recommended_roles = get_job_recommendations(resume_skills)
                if not recommended_roles: recommended_roles = [desired_role]
                
                for role in recommended_roles:
                    loc = random.choice(JOB_LOCATIONS)
                    search_query = f"{role} jobs in {loc}".replace(" ", "+")
                    # Popular job board links
                    linkedin_url = f"https://www.linkedin.com/jobs/search/?keywords={search_query}"
                    indeed_url = f"https://www.indeed.com/jobs?q={search_query}"
                    google_url = f"https://www.google.com/search?q={search_query}"
                    
                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); padding: 16px; border-radius: 12px; margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <h4 style="margin:0; color: #f8fafc;">{role}</h4>
                                <span style="color: #94a3b8; font-size: 0.9rem;">📍 {loc}</span>
                                <div style="margin-top: 4px; color: #34d399; font-size: 0.8rem; font-weight: 600;">
                                    Matched: {', '.join(set(resume_skills) & set(ROLE_SKILLS.get(role, [])))}
                                </div>
                            </div>
                            <div style="display: flex; gap: 8px;">
                                <a href="{linkedin_url}" target="_blank" class="yt-link-btn" style="padding: 6px 12px; font-size: 0.75rem;">LinkedIn</a>
                                <a href="{indeed_url}" target="_blank" class="yt-link-btn" style="padding: 6px 12px; font-size: 0.75rem; background: rgba(59, 130, 246, 0.2);">Indeed</a>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            # Phase 6: Skill Distribution
            with st.container(border=True):
                st.subheader("Skill Distribution")
                chart_data = pd.DataFrame({
                    'Skill': resume_skills + missing_for_role,
                    'Status': ['Possessed']*len(resume_skills) + ['Missing']*len(missing_for_role)
                })
                if not chart_data.empty:
                    fig = px.pie(chart_data, names='Status', hole=.6, 
                                 color='Status', color_discrete_map={'Possessed':'#10b981', 'Missing':'#ef4444'})
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='#f1f5f9', 
                                      margin=dict(t=20, b=20, l=20, r=20), showlegend=True)
                    st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("Please upload your resume to begin analysis.")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #888;'>SkillGapAI © 2026</div>", unsafe_allow_html=True)
