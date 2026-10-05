"""
AI Workforce Upskilling Platform - Interactive Web Application
For Project Review 2: Resume Intelligence, Skill Extraction, Gap Analysis & Personalized Roadmap
"""

import os
import sys
import json
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Ensure project root is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from modules.resume_parser import ResumeParser
from modules.skill_extractor import SkillExtractor
from modules.role_engine import RoleEngine
from modules.gap_analyzer import SkillGapAnalyzer
from modules.recommender import Recommender
from modules.ai_mentor import AIMentor

# Page configuration
st.set_page_config(
    page_title="AI Workforce Upskilling Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for polished, academic & enterprise presentation
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border-radius: 10px;
        padding: 1.2rem;
        border: 1px solid #E2E8F0;
        text-align: center;
    }
    .skill-pill {
        display: inline-block;
        background-color: #EFF6FF;
        color: #1D4ED8;
        padding: 4px 10px;
        border-radius: 16px;
        margin: 3px;
        font-size: 0.85rem;
        font-weight: 500;
        border: 1px solid #BFDBFE;
    }
    .skill-pill-adv {
        display: inline-block;
        background-color: #ECFDF5;
        color: #047857;
        padding: 4px 10px;
        border-radius: 16px;
        margin: 3px;
        font-size: 0.85rem;
        font-weight: 500;
        border: 1px solid #A7F3D0;
    }
    .skill-pill-interm {
        display: inline-block;
        background-color: #FEF3C7;
        color: #B45309;
        padding: 4px 10px;
        border-radius: 16px;
        margin: 3px;
        font-size: 0.85rem;
        font-weight: 500;
        border: 1px solid #FDE68A;
    }
    .skill-pill-beg {
        display: inline-block;
        background-color: #F3F4F6;
        color: #4B5563;
        padding: 4px 10px;
        border-radius: 16px;
        margin: 3px;
        font-size: 0.85rem;
        font-weight: 500;
        border: 1px solid #E5E7EB;
    }
    .status-badge-match {
        background-color: #D1FAE5;
        color: #065F46;
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: 600;
    }
    .status-badge-partial {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: 600;
    }
    .status-badge-missing {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 4px 8px;
        border-radius: 6px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize cached instances
@st.cache_resource
def load_components():
    parser = ResumeParser()
    extractor = SkillExtractor()
    role_engine = RoleEngine()
    analyzer = SkillGapAnalyzer()
    recommender = Recommender()
    mentor = AIMentor()
    return parser, extractor, role_engine, analyzer, recommender, mentor

parser, extractor, role_engine, analyzer, recommender, mentor = load_components()

# Sidebar: Controls & Inputs
st.sidebar.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=64)
st.sidebar.title("AI Upskilling Platform")
st.sidebar.caption("Final Year Capstone • Review 2 Implementation")
st.sidebar.markdown("---")

input_mode = st.sidebar.radio(
    "Choose Input Method",
    ["📁 Upload Resume (PDF / DOCX / TXT)", "⚡ Choose Sample Resume", "✍️ Paste Resume Text"]
)

resume_text = ""
resume_filename = "resume.txt"
candidate_preset_name = ""

sample_dir = os.path.join(BASE_DIR, "data", "sample_resumes")

if input_mode == "📁 Upload Resume (PDF / DOCX / TXT)":
    uploaded_file = st.sidebar.file_uploader(
        "Upload Candidate Resume",
        type=["pdf", "docx", "txt"],
        help="Upload standard PDF, Word (.docx), or plain text resume file."
    )
    if uploaded_file is not None:
        resume_filename = uploaded_file.name
        with st.spinner("Extracting resume content..."):
            resume_text = parser.extract_text_from_file(uploaded_file, uploaded_file.name)

elif input_mode == "⚡ Choose Sample Resume":
    sample_options = {
        "Alex Chen — Aspiring ML Engineer (BS in CS)": "sample_ml_engineer.txt",
        "Priya Sharma — Data Analyst (MS in Business Analytics)": "sample_data_analyst.txt",
        "Rohan Verma — Junior Developer (CS Graduate)": "sample_junior_dev.txt"
    }
    chosen_sample = st.sidebar.selectbox("Select Benchmark Candidate Profile", list(sample_options.keys()))
    sample_file_path = os.path.join(sample_dir, sample_options[chosen_sample])
    if os.path.exists(sample_file_path):
        with open(sample_file_path, "r", encoding="utf-8") as f:
            resume_text = f.read()
            resume_filename = sample_options[chosen_sample]
            candidate_preset_name = chosen_sample.split("—")[0].strip()

else:
    resume_text = st.sidebar.text_area(
        "Paste Resume Raw Text",
        height=260,
        placeholder="Paste full resume text including education, experience, and skills here..."
    )
    resume_filename = "pasted_resume.txt"

st.sidebar.markdown("---")
# Target Role Selection
roles_list = role_engine.get_all_roles()
role_dict = {r["role_title"]: r["role_id"] for r in roles_list}
selected_role_title = st.sidebar.selectbox(
    "Select Target Job Role",
    list(role_dict.keys()),
    index=0
)
selected_role_id = role_dict[selected_role_title]
selected_role_data = role_engine.get_role_by_id(selected_role_id)

st.sidebar.info(f"🎯 **Target Domain:** {selected_role_data.get('domain')}\n\n**Expected Competencies:** {len(selected_role_data.get('expected_competencies', []))} skills")

# Main Header
st.markdown('<div class="main-header">🎓 AI Workforce Upskilling Platform</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Automated Resume Intelligence, Semantic Skill Normalization, Role Competency Mapping & Personalized Upskilling Roadmap</div>', unsafe_allow_html=True)

# Verification check
if not resume_text or len(resume_text.strip()) < 50:
    st.warning("👈 Please upload a resume or select a sample candidate profile from the left sidebar to begin analysis.")
    st.markdown("""
    ### 📌 About Review 2 Deliverables:
    This prototype implements the core pipeline outlined in your Project Action Plan:
    1. **Resume Ingestion & Parsing:** Multi-format parser (PDF, DOCX, TXT) extracting contact info, degrees, and sections.
    2. **NLP Skill Extraction & Normalization:** Identifies technical competencies and maps alias synonyms to a standardized taxonomy.
    3. **Target Role Competency Benchmarking:** Pre-configured industry competency standards with importance weights (Critical, High, Medium).
    4. **Weighted Skill Gap Analysis:** Quantifies role readiness score (0-100%) and ranks missing/partial skills by urgency.
    5. **Personalized Upskilling Roadmap:** Generates phased learning paths with recommended courses, project milestones, and practice drills.
    6. **Interactive AI Mentor:** Context-aware guidance explaining why each gap matters and answering candidate career questions.
    """)
    st.stop()

# Run Pipeline
with st.spinner("Analyzing candidate profile and computing competency gap..."):
    parsed_resume = parser.parse(resume_text, resume_filename)
    if candidate_preset_name and parsed_resume["contact_info"]["name"] == "Not Detected":
        parsed_resume["contact_info"]["name"] = candidate_preset_name

    extracted_skills = extractor.extract_skills(parsed_resume["raw_text"])
    gap_analysis = analyzer.analyze_gap(extracted_skills, selected_role_data)
    roadmap = recommender.generate_roadmap(gap_analysis, selected_role_data)

candidate_name = parsed_resume["contact_info"]["name"]
if candidate_name == "Not Detected" and candidate_preset_name:
    candidate_name = candidate_preset_name

# Top Executive KPI Cards
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
with kpi1:
    st.metric("Role Readiness", f"{gap_analysis['readiness_score']}%")
with kpi2:
    st.metric("Extracted Skills", extracted_skills["total_extracted"])
with kpi3:
    st.metric("Matched Competencies", f"{gap_analysis['fully_matched_count']} / {gap_analysis['total_role_skills']}")
with kpi4:
    st.metric("Partial Upgrades", gap_analysis["partially_matched_count"])
with kpi5:
    st.metric("Critical Gaps", gap_analysis["missing_count"])

st.markdown("---")

# Navigation Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📄 Extracted Profile",
    "🎯 Role Competency",
    "📊 Skill Gap & Readiness",
    "🗺️ Upskilling Roadmap",
    "🤖 AI Career Mentor",
    "📋 Review Report"
])

# ----------------- TAB 1: Extracted Profile -----------------
with tab1:
    st.subheader("Candidate Resume Intelligence")
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("#### 👤 Contact Information")
        st.write(f"**Name:** {candidate_name}")
        st.write(f"**Email:** {parsed_resume['contact_info']['email']}")
        st.write(f"**Phone:** {parsed_resume['contact_info']['phone']}")
        if parsed_resume['contact_info']['linkedin'] != "Not Found":
            st.write(f"**LinkedIn:** [{parsed_resume['contact_info']['linkedin']}](https://{parsed_resume['contact_info']['linkedin']})")
        if parsed_resume['contact_info']['github'] != "Not Found":
            st.write(f"**GitHub:** [{parsed_resume['contact_info']['github']}](https://{parsed_resume['contact_info']['github']})")

        st.markdown("#### 🎓 Extracted Education")
        if parsed_resume["education"]:
            for edu in parsed_resume["education"]:
                st.info(f"🎓 {edu}")
        else:
            st.write("No degree mentions explicitly parsed.")

        st.markdown("#### 📈 Document Statistics")
        st.write(f"• **Word Count:** {parsed_resume['stats']['word_count']} words")
        st.write(f"• **Detected Sections:** {', '.join(parsed_resume['stats']['sections_found'])}")

    with col2:
        st.markdown("#### 💡 Extracted Competencies by Domain")
        by_cat = extracted_skills.get("skills_by_category", {})
        if not by_cat:
            st.warning("No normalized skills identified in the resume text.")
        else:
            for cat, skills in by_cat.items():
                with st.expander(f"📁 {cat} ({len(skills)} skills)", expanded=True):
                    pill_html = ""
                    for s in skills:
                        p = s["estimated_proficiency"]
                        cls_name = "skill-pill-adv" if p == "Advanced" else ("skill-pill-interm" if p == "Intermediate" else "skill-pill-beg")
                        pill_html += f'<span class="{cls_name}">{s["canonical_name"]} • <i>{p}</i></span> '
                    st.markdown(pill_html, unsafe_allow_html=True)

        st.markdown("#### 🔍 Proficiency Distribution")
        dist = extracted_skills.get("proficiency_distribution", {})
        col_d1, col_d2, col_d3 = st.columns(3)
        col_d1.metric("Advanced", dist.get("Advanced", 0))
        col_d2.metric("Intermediate", dist.get("Intermediate", 0))
        col_d3.metric("Beginner", dist.get("Beginner", 0))

# ----------------- TAB 2: Role Competency -----------------
with tab2:
    st.subheader(f"Role Benchmark: {selected_role_data['role_title']}")
    st.markdown(f"**Domain:** `{selected_role_data.get('domain')}`")
    st.write(selected_role_data.get("description", ""))

    st.markdown("#### 📌 Key Role Responsibilities")
    for resp in selected_role_data.get("responsibilities", []):
        st.markdown(f"- {resp}")

    st.markdown("#### 📋 Target Competency Benchmark Matrix")
    req_df = []
    for c in selected_role_data.get("expected_competencies", []):
        req_df.append({
            "Skill": c["canonical_name"],
            "Importance": c["importance"],
            "Weight": c["weight"],
            "Expected Proficiency": c["expected_proficiency"]
        })
    df_req = pd.DataFrame(req_df)
    st.dataframe(df_req, use_container_width=True)

# ----------------- TAB 3: Skill Gap & Readiness -----------------
with tab3:
    st.subheader("Skill Gap & Role Readiness Analytics")

    # Readiness Banner
    score = gap_analysis["readiness_score"]
    color = gap_analysis["readiness_color"]
    st.markdown(f"""
    <div style="background-color: {color}15; border-left: 6px solid {color}; padding: 16px; border-radius: 8px; margin-bottom: 20px;">
        <h3 style="margin: 0; color: {color};">Readiness: {score}% — {gap_analysis['readiness_tier']}</h3>
        <p style="margin: 5px 0 0 0; color: #334155;">{gap_analysis['verdict']}</p>
    </div>
    """, unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("#### 🕸️ Competency Alignment Radar")
        # Prepare radar chart
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
            name='Candidate Estimated Level',
            line_color='#10B981'
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 3], tickvals=[0, 1, 2, 3], ticktext=['None', 'Beginner', 'Interm', 'Adv'])),
            showlegend=True,
            margin=dict(l=40, r=40, t=20, b=20),
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)

    with chart_col2:
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
                color_discrete_map={"Critical": "#EF4444", "High": "#F59E0B", "Medium": "#3B82F6"},
                title="Level Difference (Expected Level - Candidate Level)"
            )
            fig_bar.update_layout(yaxis=dict(tickvals=[1, 2, 3], ticktext=["1 Level", "2 Levels", "3 Levels"]), height=350, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.success("🎉 No gaps detected! Candidate fully meets or exceeds all role competencies.")

    st.markdown("#### 📋 Detailed Skill Gap Breakdown Matrix")
    matrix_rows = []
    for item in matrix:
        if item["status"] == "Matched":
            status_badge = "✅ Matched"
        elif item["status"] == "Partial":
            status_badge = "⚠️ Partial Upgrade"
        else:
            status_badge = "❌ Missing"

        matrix_rows.append({
            "Competency": item["skill_name"],
            "Importance": item["importance"],
            "Status": status_badge,
            "Candidate Level": item["candidate_level"],
            "Expected Benchmark": item["expected_level"],
            "Gap Severity": f"+{item['gap']} levels" if item["gap"] > 0 else "None"
        })

    st.dataframe(pd.DataFrame(matrix_rows), use_container_width=True)

    if gap_analysis["extra_candidate_skills"]:
        st.markdown("#### 🌟 Candidate Surplus Competencies (Beyond Target Role)")
        pill_html = ""
        for s in gap_analysis["extra_candidate_skills"]:
            pill_html += f'<span class="skill-pill">{s}</span> '
        st.markdown(pill_html, unsafe_allow_html=True)

# ----------------- TAB 4: Upskilling Roadmap -----------------
with tab4:
    st.subheader(f"Personalized Upskilling Roadmap for {selected_role_data['role_title']}")
    st.caption(f"Estimated Completion: **{roadmap['summary']['estimated_completion_time']}** | Total Gaps Addressed: **{roadmap['summary']['total_gaps_addressed']}**")

    for phase in roadmap["phases"]:
        with st.expander(f"📍 {phase['title']} ({phase['estimated_time']})", expanded=True):
            st.markdown(f"**Core Focus:** *{phase['focus']}*")
            st.markdown("---")
            for item in phase["items"]:
                st.markdown(f"### 🎯 Skill: `{item['skill']}` — Target: `{item['target_level']}`")
                st.markdown(f"**Gap Diagnosis:** {item['gap_type']}")

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

# ----------------- TAB 5: AI Career Mentor -----------------
with tab5:
    st.subheader("🤖 AI Career Mentor & Diagnostic Guidance")

    # Generate diagnostic brief
    briefing = mentor.generate_mentor_briefing(candidate_name, selected_role_data["role_title"], gap_analysis)
    st.markdown(briefing)

    st.markdown("---")
    st.markdown("#### 💬 Ask the AI Mentor")
    st.write("Ask questions about your gaps, recommended portfolio projects, or role requirements:")

    quick_prompts = [
        "Why is Docker important for an ML Engineer?",
        "What hands-on portfolio project should I build first?",
        "How long will it take to become job-ready?",
        "How can I prepare for technical interviews for this role?"
    ]
    cols = st.columns(len(quick_prompts))
    user_query = ""
    for idx, prompt_text in enumerate(quick_prompts):
        if cols[idx].button(f"💡 {prompt_text[:28]}...", key=f"qp_{idx}"):
            user_query = prompt_text

    custom_query = st.text_input("Or enter your question:", value=user_query, placeholder="e.g. Why is MLOps required for Machine Learning?")

    if custom_query:
        with st.chat_message("user"):
            st.write(custom_query)
        with st.chat_message("assistant"):
            answer = mentor.answer_question(custom_query, selected_role_id, gap_analysis)
            st.markdown(answer)

# ----------------- TAB 6: Review Report -----------------
with tab6:
    st.subheader("📋 Comprehensive Review 2 Diagnostic Report")
    st.caption("Generate a formatted evaluation report for your project review presentation and submission.")

    report_lines = []
    report_lines.append(f"# AI Workforce Upskilling Platform - Evaluation Report")
    report_lines.append(f"**Date:** October 2026 | **Milestone:** Project Review 2")
    report_lines.append(f"**Candidate:** {candidate_name} | **Target Role:** {selected_role_data['role_title']}")
    report_lines.append(f"**Role Readiness Score:** {gap_analysis['readiness_score']}% ({gap_analysis['readiness_tier']})\n")
    report_lines.append("## 1. Resume Extraction Summary")
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

    st.text_area("Markdown Report Preview", full_report_text, height=350)
    st.download_button(
        "📥 Download Evaluation Report (.md)",
        data=full_report_text,
        file_name=f"Upskilling_Report_{selected_role_id}.md",
        mime="text/markdown"
    )
