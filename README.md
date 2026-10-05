# 🎓 AI Workforce Upskilling Platform
### Final Year Capstone Project — Project Review 2 Implementation

An end-to-end intelligent workforce learning and skill intelligence platform that extracts competencies from resumes, matches them against industry role benchmarks, identifies prioritized skill gaps, computes quantitative Role Readiness Scores, delivers dynamic skill assessments, and matches custom job postings using NLP.

---

## 🌟 3 Newly Added Features (Accurately Working)

Based on a detailed analysis of the **Project Report Objectives & Action Plan**, 3 advanced features have been added:

### 1. 📝 Dynamic AI Skill Assessment & Real-Time Upgrade Loop (Objective 5)
- **Problem Solved:** Conventional systems provide static gap reports without verifying if the learner actually possesses the skill or measuring improvement.
- **How It Works:** Learner takes an interactive multiple-choice & conceptual skill test tailored to the target role's competencies.
- **Closed-Loop Feedback:** When the learner scores $\ge 70\%$, their skill proficiency is **dynamically elevated in real-time** (e.g. *Beginner* $\rightarrow$ *Intermediate* $\rightarrow$ *Advanced*), the Role Readiness Score recalculates immediately, and the gap closes with celebratory feedback!

### 2. 🔍 Custom Job Description (JD) Semantic Matcher (AI/ML Framework Item 1-3)
- **Problem Solved:** Job roles evolve constantly; static role profiles alone cannot evaluate real-world job postings from LinkedIn or Indeed.
- **How It Works:** Evaluators can paste any live job description. The engine uses **NLP entity extraction** to identify required skills, computes **TF-IDF Vectorization & Cosine Semantic Similarity** between the resume text and the JD, and generates a composite alignment score (0–100%) alongside resume tailoring advice.

### 3. 🚀 Multi-Role Career Pathways & High-ROI Competency Radar (Future Scope Item 8)
- **Problem Solved:** Learners often do not know which adjacent career path best matches their current profile or which single skill gives the highest return on investment.
- **How It Works:** Analyzes the candidate profile against all industry roles simultaneously (Data Analyst, ML Engineer, AI Engineer, Software Developer, Cloud & DevOps, Cybersecurity) and ranks **Top 5 High-ROI Skills** that unlock the highest number of roles simultaneously.

---

## 🎨 User-Friendly GUI Enhancements

- **Modern Visual Theme:** Professional indigo/violet gradient hero banner, glassmorphic metric cards, and clean typography (`Plus Jakarta Sans`).
- **1-Click Benchmark Candidates:** Evaluators can test the entire pipeline in 1 click without needing to find or upload local files.
- **Interactive Visualizations:** Plotly radar charts, level-difference gap severity bars, and cross-role horizontal comparison bars.
- **Contextual Explanations:** Full question-by-question explanations in the assessment engine and interactive AI Career Mentor.

---

## 🏗️ System Architecture

```text
  [Candidate Resume (PDF/DOCX/TXT) or Sample Profile]
                          │
                          ▼
            ┌───────────────────────────┐
            │   Resume Parser Module    │  <-- Regex + NLP Section Segmenter
            └─────────────┬─────────────┘
                          │ (Cleaned text & sections)
                          ▼
            ┌───────────────────────────┐
            │  Skill Extractor & Normalizer │  <-- Taxonomy Knowledge Base (150+ aliases)
            └─────────────┬─────────────┘
                          │ (Learner Skill Profile + Estimated Proficiencies)
                          ▼
            ┌───────────────────────────┐
            │ Role Competency Benchmark │  <-- Industry Role Competency Profiles
            └─────────────┬─────────────┘
                          │
                          ▼
            ┌───────────────────────────┐
            │    Skill Gap Analyzer     │  <-- Weighted Scoring Algorithm
            └──────┬─────────────┬──────┘
                   │             │
        ┌──────────┴──┐       ┌──┴──────────────────────────────────────┐
        ▼             ▼       ▼             ▼              ▼            ▼
   [Readiness   [Prioritized  [Phased     [Skill Assessment [Custom JD   [Multi-Role
     Score]        Gaps]      Roadmap]     Quiz & Upgrade]   Matcher]    Pathways]
```

---

## 📁 Directory Structure

```
ai_upskilling_platform/
├── app.py                      # Modern Streamlit Interactive Web Application
├── run_app.bat                 # One-click Windows Launcher
├── push_to_github.bat          # One-click GitHub Push Script
├── requirements.txt            # Dependencies
├── README.md                   # Full Documentation & Review 2 Guide
├── data/
│   ├── skills_taxonomy.json    # Standardized skills, categories, and synonym aliases
│   ├── role_competencies.json  # Benchmark competencies, importance weights & proficiencies
│   ├── learning_resources.json # Curated courses, portfolio projects & practice drills
│   ├── assessment_questions.json # Dynamic technical quiz question bank
│   └── sample_resumes/         # Built-in demo resumes for immediate testing
│       ├── sample_ml_engineer.txt
│       ├── sample_data_analyst.txt
│       └── sample_junior_dev.txt
├── modules/
│   ├── __init__.py
│   ├── resume_parser.py        # PDF, DOCX, TXT parser & section extractor
│   ├── skill_extractor.py      # Synonym normalizer & proficiency estimator
│   ├── role_engine.py          # Role competency benchmark query engine
│   ├── gap_analyzer.py         # Weighted gap & readiness score algorithm
│   ├── recommender.py          # Phased personalized roadmap generator
│   ├── ai_mentor.py            # Diagnostic briefing & contextual mentoring
│   ├── assessment_engine.py    # (NEW) Skill testing & dynamic proficiency upgrade loop
│   ├── jd_matcher.py           # (NEW) TF-IDF & Cosine similarity custom JD matcher
│   └── career_analytics.py     # (NEW) Cross-role pathways & high-ROI skill radar
└── tests/
    ├── __init__.py
    └── test_pipeline.py        # Automated test suite (7 unit tests passing)
```

---

## 🚀 How to Run the Application

1. Open PowerShell or Terminal:
   ```powershell
   cd C:\Users\YASH\OneDrive\Desktop\ai_upskilling_platform
   ```
2. Run Automated Verification Tests:
   ```powershell
   python tests/test_pipeline.py
   ```
   *(All 7 unit tests will report `OK`)*
3. Launch the Web App:
   Double-click `run_app.bat` or execute:
   ```powershell
   python -m streamlit run app.py
   ```
   Access in browser at: **`http://localhost:8501`**
