"""
AI Workforce Upskilling Platform - Next-Gen Modern Web Dashboard
Review 2 Implementation featuring:
1. Multi-format Resume Ingestion & NLP Skill Normalization
2. Role Competency Benchmarking & Weighted Gap Analytics
3. Feature 1 (NEW): Dynamic AI Skill Assessment & Real-Time Proficiency Upgrade Loop
4. Feature 2 (NEW): Custom Job Description (JD) Semantic Matcher (TF-IDF & Cosine Similarity)
5. Feature 3 (NEW): Multi-Role Career Pathways & High-ROI Skill Radar
6. Personalized Phased Learning Roadmap & AI Career Mentor
"""

import os
import sys
import copy
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Ensure base directory is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from modules.resume_parser import ResumeParser
from modules.skill_extractor import SkillExtractor
from modules.role_engine import RoleEngine
from modules.gap_analyzer import SkillGapAnalyzer
from modules.recommender import Recommender
from modules.ai_mentor import AIMentor
from modules.assessment_engine import AssessmentEngine
from modules.jd_matcher import JDMatcher
from modules.career_analytics import CareerAnalytics

# Page configuration
st.set_page_config(
    page_title="AI Workforce Upskilling Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Custom CSS Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Hero Gradient & Typography */
    .hero-container {
        background: linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #4338CA 100%);
        padding: 2.2rem 2.5rem;
        border-radius: 18px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(67, 56, 202, 0.25);
    }
    .hero-title {
        font-size: 2.25rem;
        font-weight: 800;
        letter-spacing: -0.025em;
        margin-bottom: 0.4rem;
        color: #FFFFFF;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #C7D2FE;
        font-weight: 400;
        max-width: 900px;
        line-height: 1.5;
    }
    .hero-tag {
        display: inline-block;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(8px);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        border: 1px solid rgba(255, 255, 255, 0.25);
    }

    /* Glassmorphism Metric Cards */
    .metric-box {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 1.25rem 1rem;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
    }
    .metric-val {
        font-size: 1.85rem;
        font-weight: 800;
        color: #1E293B;
        margin-top: 4px;
    }
    .metric-lbl {
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748B;
    }

    /* Modern Badges for Skills */
    .skill-pill {
        display: inline-flex;
        align-items: center;
        padding: 5px 12px;
        border-radius: 9999px;
        margin: 3px;
        font-size: 0.82rem;
        font-weight: 600;
        transition: all 0.15s ease;
    }
    .skill-adv {
        background: #ECFDF5;
        color: #047857;
        border: 1px solid #A7F3D0;
    }
    .skill-interm {
        background: #EFF6FF;
        color: #1D4ED8;
        border: 1px solid #BFDBFE;
    }
    .skill-beg {
        background: #F8FAFC;
        color: #475569;
        border: 1px solid #E2E8F0;
    }
    .skill-upgrade {
        background: #FEF3C7;
        color: #B45309;
        border: 1px solid #FDE68A;
        font-weight: 700;
    }

    /* Section Cards */
    .content-card {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 1.5rem;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
        margin-bottom: 1.5rem;
    }

    /* Custom Radio & Buttons */
    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
        padding: 0.5rem 1.25rem;
        border: none;
        transition: all 0.2s;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(67, 56, 202, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Cache components
@st.cache_resource
def load_all_engines():
    parser = ResumeParser()
    extractor = SkillExtractor()
    role_engine = RoleEngine()
    analyzer = SkillGapAnalyzer()
    recommender = Recommender()
    mentor = AIMentor()
    assessment = AssessmentEngine()
    jd_matcher = JDMatcher(extractor)
    career_analytics = CareerAnalytics(role_engine, analyzer)
    return parser, extractor, role_engine, analyzer, recommender, mentor, assessment, jd_matcher, career_analytics

parser, extractor, role_engine, analyzer, recommender, mentor, assessment, jd_matcher, career_analytics = load_all_engines()

# Manage Session State for Live Proficiency Upgrades (Feature 1 Closed Loop)
if "skill_upgrades" not in st.session_state:
    st.session_state.skill_upgrades = {}
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "quiz_results" not in st.session_state:
    st.session_state.quiz_results = None

# Sidebar Configuration
st.sidebar.markdown("""
<div style="text-align: center; padding: 10px 0;">
    <h2 style="margin: 0; color: #1E293B; font-weight: 800;">⚡ TalentAI</h2>
    <p style="margin: 0; color: #64748B; font-size: 0.85rem;">Workforce Upskilling & Skill Intelligence</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

input_mode = st.sidebar.radio(
    "📥 Select Resume Source",
    ["⚡ 1-Click Benchmark Candidates", "📁 Upload Resume (PDF / Word / TXT)", "✍️ Paste Resume Text"]
)

resume_text = ""
resume_filename = "resume.txt"
candidate_preset_name = ""
sample_dir = os.path.join(BASE_DIR, "data", "sample_resumes")

if input_mode == "⚡ 1-Click Benchmark Candidates":
    sample_options = {
        "Alex Chen — Aspiring ML Engineer (UC Berkeley)": "sample_ml_engineer.txt",
        "Priya Sharma — Data Analyst (NYU MS Analytics)": "sample_data_analyst.txt",
        "Rohan Verma — Junior Developer (CS Graduate)": "sample_junior_dev.txt"
    }
    chosen_sample = st.sidebar.selectbox("Select Candidate Profile", list(sample_options.keys()))
    sample_file_path = os.path.join(sample_dir, sample_options[chosen_sample])
    if os.path.exists(sample_file_path):
        with open(sample_file_path, "r", encoding="utf-8") as f:
            resume_text = f.read()
            resume_filename = sample_options[chosen_sample]
            candidate_preset_name = chosen_sample.split("—")[0].strip()

elif input_mode == "📁 Upload Resume (PDF / Word / TXT)":
    uploaded_file = st.sidebar.file_uploader(
        "Upload Resume Document",
        type=["pdf", "docx", "txt"],
        help="Upload PDF, DOCX, or TXT file"
    )
    if uploaded_file is not None:
        resume_filename = uploaded_file.name
        with st.spinner("Extracting resume contents..."):
            resume_text = parser.extract_text_from_file(uploaded_file, uploaded_file.name)

else:
    resume_text = st.sidebar.text_area(
        "Paste Resume Text",
        height=220,
        placeholder="Paste full candidate resume here..."
    )
    resume_filename = "pasted_resume.txt"

st.sidebar.markdown("---")

# Target Role Selection
roles_list = role_engine.get_all_roles()
role_dict = {r["role_title"]: r["role_id"] for r in roles_list}
selected_role_title = st.sidebar.selectbox(
    "🎯 Select Target Job Role",
    list(role_dict.keys()),
    index=0
)
selected_role_id = role_dict[selected_role_title]
selected_role_data = role_engine.get_role_by_id(selected_role_id)

st.sidebar.caption(f"**Domain:** {selected_role_data.get('domain')}")
st.sidebar.caption(f"**Benchmark Skills:** {len(selected_role_data.get('expected_competencies', []))} competencies")

if st.session_state.skill_upgrades:
    st.sidebar.success(f"⚡ {len(st.session_state.skill_upgrades)} skill(s) upgraded via quiz!")
    if st.sidebar.button("🔄 Reset Quiz Upgrades"):
        st.session_state.skill_upgrades = {}
        st.session_state.quiz_submitted = False
        st.session_state.quiz_results = None
        st.rerun()

# Hero Banner
st.markdown("""
<div class="hero-container">
    <div class="hero-tag">CAPSTONE PROJECT REVIEW 2 • SKILL-CENTRIC UPSKILLING</div>
    <div class="hero-title">AI Workforce Upskilling & Career Readiness Platform</div>
    <div class="hero-subtitle">
        Shifting from conventional course completion to quantitative competency intelligence: Automated Resume Parsing, 
        Taxonomy Normalization, Weighted Gap Analysis, Phased Roadmaps, Custom JD Matching, and Closed-Loop Skill Assessments.
    </div>
</div>
""", unsafe_allow_html=True)

if not resume_text or len(resume_text.strip()) < 40:
    st.info("👈 Select a benchmark profile or upload a resume from the left sidebar to start the analysis.")
    st.stop()

# Execution Pipeline
with st.spinner("Executing skill intelligence pipeline..."):
    parsed_resume = parser.parse(resume_text, resume_filename)
    if candidate_preset_name and parsed_resume["contact_info"]["name"] == "Not Detected":
        parsed_resume["contact_info"]["name"] = candidate_preset_name

    candidate_name = parsed_resume["contact_info"]["name"]
    if candidate_name == "Not Detected" and candidate_preset_name:
        candidate_name = candidate_preset_name

    # Extract skills
    extracted_skills = extractor.extract_skills(parsed_resume["raw_text"])

    # Apply any live upgrades earned in the assessment quiz (Feature 1)
    if st.session_state.skill_upgrades:
        extracted_skills = copy.deepcopy(extracted_skills)
        for s_id, up_info in st.session_state.skill_upgrades.items():
            if s_id in extracted_skills["skills"]:
                extracted_skills["skills"][s_id]["estimated_proficiency"] = up_info["awarded_proficiency"]
            else:
                extracted_skills["skills"][s_id] = {
                    "id": s_id,
                    "canonical_name": up_info["skill_name"],
                    "category": "Assessed Competencies",
                    "estimated_proficiency": up_info["awarded_proficiency"],
                    "frequency": 1,
                    "context_snippets": ["Demonstrated competency via live assessment quiz."]
                }
        extracted_skills["total_extracted"] = len(extracted_skills["skills"])

    # Compute Gap Analysis & Roadmap
    gap_analysis = analyzer.analyze_gap(extracted_skills, selected_role_data)
    roadmap = recommender.generate_roadmap(gap_analysis, selected_role_data)

# KPI Metrics Ribbon
m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    readiness_delta = f"+{len(st.session_state.skill_upgrades)*4}% (Quiz)" if st.session_state.skill_upgrades else None
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-lbl">Role Readiness</div>
        <div class="metric-val" style="color: {gap_analysis['readiness_color']};">{gap_analysis['readiness_score']}%</div>
    </div>
    """, unsafe_allow_html=True)
with m2:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-lbl">Identified Skills</div>
        <div class="metric-val">{extracted_skills['total_extracted']}</div>
    </div>
    """, unsafe_allow_html=True)
with m3:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-lbl">Role Matches</div>
        <div class="metric-val" style="color: #10B981;">{gap_analysis['fully_matched_count']} / {gap_analysis['total_role_skills']}</div>
    </div>
    """, unsafe_allow_html=True)
with m4:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-lbl">Partial Upgrades</div>
        <div class="metric-val" style="color: #F59E0B;">{gap_analysis['partially_matched_count']}</div>
    </div>
    """, unsafe_allow_html=True)
with m5:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-lbl">Critical Gaps</div>
        <div class="metric-val" style="color: #EF4444;">{gap_analysis['missing_count']}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

# Main Navigation Tabs (Including the 3 NEW Features)
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📄 Extracted Profile",
    "🎯 Benchmark & Gap Analysis",
    "📝 1. Live Skill Quiz & Dynamic Upgrade",
    "🔍 2. Custom JD Semantic Matcher",
    "🚀 3. Multi-Role Pathways & ROI",
    "🗺️ Phased Roadmap",
    "🤖 AI Career Mentor",
    "📥 Review Report"
])

# ----------------- TAB 1: Extracted Profile -----------------
with tab1:
    st.markdown("### 📄 Candidate Profile & Normalization Intelligence")
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("#### 👤 Candidate Credentials")
        st.write(f"**Name:** {candidate_name}")
        st.write(f"**Email:** `{parsed_resume['contact_info']['email']}`")
        st.write(f"**Phone:** `{parsed_resume['contact_info']['phone']}`")
        if parsed_resume['contact_info']['linkedin'] != "Not Found":
            st.write(f"**LinkedIn:** [{parsed_resume['contact_info']['linkedin']}](https://{parsed_resume['contact_info']['linkedin']})")
        if parsed_resume['contact_info']['github'] != "Not Found":
            st.write(f"**GitHub:** [{parsed_resume['contact_info']['github']}](https://{parsed_resume['contact_info']['github']})")

        st.markdown("---")
        st.markdown("#### 🎓 Academic Qualifications")
        if parsed_resume["education"]:
            for edu in parsed_resume["education"]:
                st.markdown(f"🎓 **{edu}**")
        else:
            st.caption("No explicit degree keywords matched.")

        st.markdown("---")
        st.markdown("#### 📊 Document Summary")
        st.write(f"• **Word Count:** {parsed_resume['stats']['word_count']} words")
        st.write(f"• **Detected Sections:** {len(parsed_resume['stats']['sections_found'])}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("#### 🏷️ Normalized Skills by Competency Domain")
        by_cat = extracted_skills.get("skills_by_category", {})
        if not by_cat:
            st.warning("No normalized skills identified.")
        else:
            for cat, skills in by_cat.items():
                with st.expander(f"📁 {cat} ({len(skills)} competencies)", expanded=True):
                    pill_html = ""
                    for s in skills:
                        p = s["estimated_proficiency"]
                        cls_name = "skill-adv" if p == "Advanced" else ("skill-interm" if p == "Intermediate" else "skill-beg")
                        pill_html += f'<span class="skill-pill {cls_name}">{s["canonical_name"]} <small style="opacity: 0.8; margin-left: 4px;">• {p}</small></span> '
                    st.markdown(pill_html, unsafe_allow_html=True)

        st.markdown("#### 📈 Proficiency Breakdown")
        dist = extracted_skills.get("proficiency_distribution", {})
        c1, c2, c3 = st.columns(3)
        c1.metric("Advanced (Proficient)", dist.get("Advanced", 0))
        c2.metric("Intermediate (Working)", dist.get("Intermediate", 0))
        c3.metric("Beginner (Foundational)", dist.get("Beginner", 0))
        st.markdown('</div>', unsafe_allow_html=True)

# ----------------- TAB 2: Benchmark & Gap Analysis -----------------
with tab2:
    st.markdown(f"### 🎯 Competency Gap Analysis: **{selected_role_data['role_title']}**")

    # Readiness Alert
    score = gap_analysis["readiness_score"]
    color = gap_analysis["readiness_color"]
    st.markdown(f"""
    <div style="background-color: {color}15; border-left: 6px solid {color}; padding: 18px 24px; border-radius: 12px; margin-bottom: 22px;">
        <h3 style="margin: 0; color: {color}; font-weight: 800;">Readiness: {score}% — {gap_analysis['readiness_tier']}</h3>
        <p style="margin: 6px 0 0 0; color: #334155; font-size: 0.98rem;">{gap_analysis['verdict']}</p>
    </div>
    """, unsafe_allow_html=True)

    gcol1, gcol2 = st.columns(2)

    with gcol1:
        st.markdown("#### 🕸️ Competency Radar (Candidate vs Benchmark)")
        matrix = gap_analysis["detailed_matrix"]
        radar_categories = [m["skill_name"] for m in matrix[:8]]
        expected_vals = [m["expected_val"] for m in matrix[:8]]
        candidate_vals = [m["candidate_val"] for m in matrix[:8]]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=expected_vals + [expected_vals[0]],
            theta=radar_categories + [radar_categories[0]],
            fill='toself',
            name='Target Role Benchmark',
            line_color='#6366F1'
        ))
        fig.add_trace(go.Scatterpolar(
            r=candidate_vals + [candidate_vals[0]],
            theta=radar_categories + [radar_categories[0]],
            fill='toself',
            name='Candidate Level',
            line_color='#10B981'
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 3], tickvals=[0, 1, 2, 3], ticktext=['None', 'Beginner', 'Interm', 'Adv'])),
            showlegend=True,
            margin=dict(l=30, r=30, t=20, b=20),
            height=340
        )
        st.plotly_chart(fig, use_container_width=True)

    with gcol2:
        st.markdown("#### 📊 Proficiency Gap Severity")
        gap_bars = [
            {"Skill": m["skill_name"], "Gap": m["gap"], "Importance": m["importance"]}
            for m in matrix if m["gap"] > 0
        ]
        if gap_bars:
            gap_df = pd.DataFrame(gap_bars).sort_values("Gap", ascending=False)
            fig_bar = px.bar(
                gap_df,
                x="Skill",
                y="Gap",
                color="Importance",
                color_discrete_map={"Critical": "#EF4444", "High": "#F59E0B", "Medium": "#3B82F6"}
            )
            fig_bar.update_layout(yaxis=dict(tickvals=[1, 2, 3], ticktext=["1 Level", "2 Levels", "3 Levels"]), height=340, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.success("🎉 Candidate meets or exceeds all role competencies!")

    st.markdown("#### 📋 Detailed Competency Breakdown")
    matrix_rows = []
    for item in matrix:
        status_label = "✅ Matched" if item["status"] == "Matched" else ("⚠️ Partial" if item["status"] == "Partial" else "❌ Missing")
        matrix_rows.append({
            "Competency": item["skill_name"],
            "Importance": item["importance"],
            "Weight": item["weight"],
            "Status": status_label,
            "Candidate Level": item["candidate_level"],
            "Expected Benchmark": item["expected_level"],
            "Gap Severity": f"+{item['gap']} levels" if item["gap"] > 0 else "None"
        })
    st.dataframe(pd.DataFrame(matrix_rows), use_container_width=True)

# ----------------- TAB 3: FEATURE 1 (NEW) Assessment Quiz & Dynamic Upgrades -----------------
with tab3:
    st.markdown("### 📝 Dynamic AI Skill Assessment & Real-Time Upgrade Loop")
    st.caption("Fulfilling Project Objective 5: Validates learner skill proficiency through interactive testing and closes the learning feedback loop by recalculating role readiness in real-time.")

    quiz_questions = assessment.get_questions_for_role(selected_role_data, max_questions=5)

    if not quiz_questions:
        st.info("No assessment questions configured for this specific role yet.")
    else:
        st.markdown(f"**Skill Test:** {len(quiz_questions)} curated questions covering core role competencies.")

        with st.form("assessment_quiz_form"):
            user_quiz_answers = {}
            for idx, q in enumerate(quiz_questions):
                st.markdown(f"#### Q{idx+1}. `{q['skill_name']}` ({q['level']} Level)")
                st.write(q["question"])
                choice = st.radio(
                    f"Select answer for Q{idx+1}:",
                    options=range(len(q["options"])),
                    format_func=lambda x: q["options"][x],
                    key=f"quiz_opt_{q['id']}"
                )
                user_quiz_answers[q["id"]] = choice
                st.markdown("---")

            submit_quiz = st.form_submit_button("⚡ Submit Assessment & Update Skill Profile", type="primary")

        if submit_quiz:
            result = assessment.evaluate_quiz(user_quiz_answers, quiz_questions)
            st.session_state.quiz_results = result
            st.session_state.quiz_submitted = True

            # Apply upgrades
            if result["upgrades"]:
                for s_id, up_val in result["upgrades"].items():
                    st.session_state.skill_upgrades[s_id] = up_val
                st.balloons()
                st.rerun()

        # Display results if available
        if st.session_state.quiz_results:
            res = st.session_state.quiz_results
            st.markdown("### 🎯 Assessment Results")
            sc_col1, sc_col2 = st.columns(2)
            sc_col1.metric("Quiz Score", f"{res['score']} / {res['total']}", f"{res['accuracy_pct']}% Accuracy")
            sc_col2.metric("Assessment Outcome", "PASSED ✅" if res["passed"] else "NEEDS REVIEW ⚠️")

            if res["upgrades"]:
                st.success("🎉 **Competency Upgrades Earned!** The following skills have been elevated in your candidate profile:")
                for s_id, up_item in res["upgrades"].items():
                    st.markdown(f"- 🌟 **{up_item['skill_name']}** $\\rightarrow$ Upgraded to **{up_item['awarded_proficiency']}**!")

            with st.expander("📖 View Question-by-Question Explanations", expanded=True):
                for d in res["details"]:
                    icon = "✅" if d["is_correct"] else "❌"
                    st.markdown(f"**{icon} {d['skill_name']} ({d['level']})**")
                    st.write(f"**Question:** {d['question_text']}")
                    st.write(f"• **Your Choice:** {d['user_selected']}")
                    st.write(f"• **Correct Option:** {d['correct_option']}")
                    st.info(f"💡 **Explanation:** {d['explanation']}")
                    st.markdown("---")

# ----------------- TAB 4: FEATURE 2 (NEW) Custom JD Matcher -----------------
with tab4:
    st.markdown("### 🔍 Custom Job Description (JD) Semantic Matcher")
    st.caption("Fulfilling AI/ML Framework Item 1-3: Analyzes any external job posting from LinkedIn or Indeed, extracts required competencies using NLP, and computes TF-IDF Cosine Similarity.")

    jd_sample_presets = {
        "Custom (Paste your own)": "",
        "Senior ML Engineer (Uber / Amazon)": """We are seeking a Machine Learning Engineer to join our Core AI team.
Responsibilities:
- Build, optimize, and deploy deep learning models using Python and PyTorch.
- Experience with Docker, Kubernetes, and FastAPI for real-time model serving.
- Experience with MLOps pipelines, MLflow, and automated model retraining.
- Proficient in SQL, relational databases, and AWS infrastructure (EC2, S3, SageMaker).
- Strong understanding of algorithms, data structures, and CI/CD pipelines.""",
        "Business Data Analyst (Retail / Fintech)": """We are hiring a Senior Data Analyst.
Key Requirements:
- 3+ years writing complex SQL queries (Window functions, CTEs, self-joins) on PostgreSQL.
- Expert in creating interactive dashboards in Tableau and Microsoft Power BI.
- Advanced Microsoft Excel capabilities including Pivot Tables, INDEX/MATCH, and macros.
- Scripting in Python using Pandas, NumPy, and Matplotlib for exploratory data analysis.
- Experience with statistical hypothesis testing, A/B testing, and cross-functional communication."""
    }

    selected_jd_preset = st.selectbox("Load Sample Job Posting or Paste Your Own:", list(jd_sample_presets.keys()))
    preset_text = jd_sample_presets[selected_jd_preset]

    jd_input_text = st.text_area(
        "Job Description Text:",
        value=preset_text,
        height=200,
        placeholder="Paste full job description text here..."
    )

    if st.button("🚀 Analyze Alignment with Candidate Resume", type="primary"):
        if len(jd_input_text.strip()) < 30:
            st.error("Please provide a valid job description.")
        else:
            with st.spinner("Calculating semantic TF-IDF overlap and keyword extraction..."):
                jd_res = jd_matcher.analyze_jd(jd_input_text, parsed_resume, extracted_skills)

            jc1, jc2, jc3 = st.columns(3)
            jc1.metric("Composite Match Score", f"{jd_res['composite_match_score']}%")
            jc2.metric("Skill Coverage", f"{jd_res['skill_coverage_pct']}%", f"{jd_res['matched_skills_count']} of {jd_res['total_jd_skills_found']} skills")
            jc3.metric("Semantic Similarity (TF-IDF)", f"{jd_res['semantic_similarity_pct']}%")

            st.markdown("---")
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.markdown("#### ✅ Matched Requirements in Resume")
                if jd_res["matched_skills"]:
                    for m in jd_res["matched_skills"]:
                        st.markdown(f"- **{m['skill_name']}** (`{m['category']}`) • *Candidate Level: {m['candidate_proficiency']}*")
                else:
                    st.write("No direct technical competencies matched.")

            with col_m2:
                st.markdown("#### ❌ Missing JD Competencies")
                if jd_res["missing_skills"]:
                    for m in jd_res["missing_skills"]:
                        st.markdown(f"- ⚠️ **{m['skill_name']}** (`{m['category']}`)")
                else:
                    st.success("🎉 All technical skills in the JD are represented on candidate's resume!")

            st.markdown("#### 💡 Resume Tailoring Strategy")
            for rec in jd_res["recommendations"]:
                st.info(f"💡 {rec}")

# ----------------- TAB 5: FEATURE 3 (NEW) Multi-Role Pathways & High ROI Skills -----------------
with tab5:
    st.markdown("### 🚀 Multi-Role Career Pathways & High-ROI Skill Radar")
    st.caption("Fulfilling Learning Analytics & Future Scope Item 8: Evaluates candidate competencies across all industry career paths simultaneously and highlights which single skill provides the highest return on investment.")

    with st.spinner("Analyzing cross-role fit..."):
        career_res = career_analytics.analyze_all_roles(extracted_skills)

    c_roles = career_res["role_evaluations"]
    best_role = career_res["best_match_role"]

    st.markdown(f"""
    <div style="background: #F0FDF4; border: 1px solid #BBF7D0; padding: 16px 20px; border-radius: 12px; margin-bottom: 20px;">
        <h4 style="margin: 0; color: #166534;">🌟 Highest Natural Role Fit: <b>{best_role['role_title']}</b> ({best_role['readiness_score']}%)</h4>
        <p style="margin: 4px 0 0 0; color: #15803D; font-size: 0.9rem;">
            Based on the candidate's existing background, this profile demonstrates the shortest time-to-hire in <b>{best_role['role_title']}</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Multi-Role Bar Comparison Chart
    role_names = [r["role_title"] for r in c_roles]
    role_scores = [r["readiness_score"] for r in c_roles]
    role_df = pd.DataFrame({"Job Role": role_names, "Readiness Score (%)": role_scores})
    
    fig_roles = px.bar(
        role_df,
        x="Readiness Score (%)",
        y="Job Role",
        orientation="h",
        color="Readiness Score (%)",
        color_continuous_scale="Blues",
        title="Candidate Readiness Across All Tech Disciplines"
    )
    fig_roles.update_layout(height=320, margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_roles, use_container_width=True)

    # Highest ROI Skills Table
    st.markdown("#### 💎 Top 5 'High-ROI' Competencies (Unlock the Most Roles)")
    st.write("Acquiring any of these skills immediately boosts your readiness score across multiple roles simultaneously:")

    roi_rows = []
    for s in career_res["highest_roi_skills"]:
        roi_rows.append({
            "High-ROI Competency": s["skill_name"],
            "Roles Unlocked / Impacted": len(s["roles_impacted"]),
            "Impacted Roles": ", ".join(s["roles_impacted"]),
            "Strategic Advantage": "Broad cross-domain utility in Modern Engineering"
        })
    st.dataframe(pd.DataFrame(roi_rows), use_container_width=True)

# ----------------- TAB 6: Phased Roadmap -----------------
with tab6:
    st.markdown(f"### 🗺️ Prioritized Upskilling Roadmap for **{selected_role_data['role_title']}**")
    st.caption(f"Estimated Completion: **{roadmap['summary']['estimated_completion_time']}** • Total Addressed Gaps: **{roadmap['summary']['total_gaps_addressed']}**")

    for phase in roadmap["phases"]:
        with st.expander(f"📍 {phase['title']} — `{phase['estimated_time']}`", expanded=True):
            st.markdown(f"**Core Objective:** *{phase['focus']}*")
            st.markdown("---")
            for item in phase["items"]:
                st.markdown(f"#### 🎯 Skill: `{item['skill']}` $\\rightarrow$ Target: `{item['target_level']}`")
                st.caption(f"Gap Diagnosis: {item['gap_type']}")

                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    st.markdown("##### 📚 Recommended Courses & Certifications")
                    if item.get("courses"):
                        for c in item["courses"]:
                            st.markdown(f"- **{c.get('title')}** ({c.get('provider')}) — `{c.get('duration', 'Self-paced')}`")
                    else:
                        st.write("Review official framework documentation and curated guides.")

                with col_c2:
                    st.markdown("##### 🛠️ Hands-on Portfolio Projects")
                    if item.get("projects"):
                        for p in item["projects"]:
                            st.markdown(f"- 🚀 {p}")
                    else:
                        st.write("Implement standard integration test microservices.")

                if item.get("practice"):
                    st.info(f"💡 **Practice Assessment Drill:** {item['practice']}")
                st.markdown("---")

# ----------------- TAB 7: AI Career Mentor -----------------
with tab7:
    st.markdown("### 🤖 Conversational AI Career Mentor")

    # Generate diagnostic brief
    briefing = mentor.generate_mentor_briefing(candidate_name, selected_role_data["role_title"], gap_analysis)
    st.markdown(briefing)

    st.markdown("---")
    st.markdown("#### 💬 Ask the AI Mentor")
    quick_prompts = [
        "Why is Docker important for an ML Engineer?",
        "What hands-on portfolio project should I build first?",
        "How long will it take to become job-ready?",
        "How can I prepare for technical interviews for this role?"
    ]
    cols = st.columns(len(quick_prompts))
    user_query = ""
    for idx, prompt_text in enumerate(quick_prompts):
        if cols[idx].button(f"💡 {prompt_text[:28]}...", key=f"qprompt_{idx}"):
            user_query = prompt_text

    custom_query = st.text_input("Or type your question:", value=user_query, placeholder="e.g. Why is MLOps required for Machine Learning?")

    if custom_query:
        with st.chat_message("user"):
            st.write(custom_query)
        with st.chat_message("assistant"):
            answer = mentor.answer_question(custom_query, selected_role_id, gap_analysis)
            st.markdown(answer)

# ----------------- TAB 8: Review Report -----------------
with tab8:
    st.markdown("### 📋 Capstone Review 2 Diagnostic Report")
    st.caption("Auto-generated comprehensive evaluation report ready for submission to your review panel.")

    report_lines = []
    report_lines.append(f"# AI Workforce Upskilling Platform - Evaluation Report")
    report_lines.append(f"**Milestone:** Capstone Project Review 2 | **Date:** October 2026")
    report_lines.append(f"**Candidate Name:** {candidate_name} | **Target Role:** {selected_role_data['role_title']}")
    report_lines.append(f"**Role Readiness Score:** {gap_analysis['readiness_score']}% ({gap_analysis['readiness_tier']})\n")
    report_lines.append("## 1. Resume Ingestion & Parsing")
    report_lines.append(f"- **Email:** {parsed_resume['contact_info']['email']}")
    report_lines.append(f"- **Phone:** {parsed_resume['contact_info']['phone']}")
    report_lines.append(f"- **Total Identified Competencies:** {extracted_skills['total_extracted']}")
    report_lines.append(f"- **Education:** {', '.join(parsed_resume['education']) if parsed_resume['education'] else 'N/A'}\n")
    report_lines.append("## 2. Competency Gap Analysis")
    report_lines.append(f"- **Matched Role Skills:** {gap_analysis['fully_matched_count']} / {gap_analysis['total_role_skills']}")
    report_lines.append(f"- **Partial Proficiency Upgrades:** {gap_analysis['partially_matched_count']}")
    report_lines.append(f"- **Missing Critical Competencies:** {gap_analysis['missing_count']}\n")
    report_lines.append("### Prioritized Gaps:")
    for g in gap_analysis["prioritized_gaps"]:
        report_lines.append(f"- **[{g['priority_label']}]** {g['skill_name']} -> Target: {g['target_level']}")
    report_lines.append("\n## 3. Recommended Upskilling Roadmap")
    report_lines.append(f"- **Estimated Timeline:** {roadmap['summary']['estimated_completion_time']}")
    for ph in roadmap["phases"]:
        report_lines.append(f"### {ph['title']}")
        for it in ph["items"]:
            report_lines.append(f"- **{it['skill']}**: {it['gap_type']}")
            if it.get("projects"):
                report_lines.append(f"  - Recommended Project: {it['projects'][0]}")

    full_report_text = "\n".join(report_lines)

    st.text_area("Markdown Report Preview", full_report_text, height=300)
    st.download_button(
        "📥 Download Evaluation Report (.md)",
        data=full_report_text,
        file_name=f"Upskilling_Evaluation_Report_{selected_role_id}.md",
        mime="text/markdown",
        type="primary"
    )
