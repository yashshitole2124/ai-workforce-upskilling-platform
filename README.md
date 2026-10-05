# 🎓 AI Workforce Upskilling Platform
### Final Year Capstone Project — Implementation for Project Review 2

An end-to-end intelligent learning and workforce-development system that extracts competencies from candidate resumes, matches them against industry role benchmarks, identifies prioritized skill gaps, computes a quantitative Role Readiness Score, and generates a personalized upskilling roadmap.

---

## 📌 Project Review 2 Scope & Objectives Met

According to the Project Action Plan:
- **Phase 1 & 2 (Taxonomy & Role Profiles):** Standardized skill taxonomy across 9 domains with 150+ aliases/synonyms; benchmark competency matrices for industry roles (ML Engineer, Data Analyst, AI/GenAI Engineer, Software Developer, Cloud & DevOps, Cybersecurity).
- **Phase 3 (Resume Parsing & Skill Extraction):** Multi-format parser supporting **PDF, DOCX, and TXT**, extracting candidate contact info, degrees, and sections. Semantic skill extraction with alias normalization and context-based proficiency estimation.
- **Phase 4 (Skill Gap & Readiness Engine):** Weighted competency gap analysis, proficiency level comparison, prioritized gap ranking ($P_1$ Critical, $P_2$ High, $P_3$ Medium), and overall Role Readiness percentage ($0-100\%$).
- **Personalized Roadmap Prototype:** Dynamic multi-phase upskilling plan recommending targeted courses, certifications, and portfolio projects.
- **Conversational AI Mentor:** Context-aware diagnostics and Q&A explaining the rationale behind critical skill gaps.

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
        ┌──────────┴──┐       ┌──┴──────────┐
        ▼             ▼       ▼             ▼
   [Readiness   [Prioritized  [Personalized  [AI Career Mentor
     Score]        Gaps]       Roadmap]       Guidance & Q&A]
```

---

## 📁 Project Structure

```
ai_upskilling_platform/
├── app.py                      # Main Streamlit Interactive Web Application
├── run_app.bat                 # One-click Windows Launcher
├── requirements.txt            # Python dependencies
├── README.md                   # Complete documentation & Viva Guide
├── data/
│   ├── skills_taxonomy.json    # Standardized skills, categories, and synonym aliases
│   ├── role_competencies.json  # Benchmark competencies, importance weights & proficiencies
│   ├── learning_resources.json # Curated courses, portfolio projects & practice drills
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
│   └── ai_mentor.py            # Diagnostic briefing & contextual mentoring
└── tests/
    ├── __init__.py
    └── test_pipeline.py        # Automated unit test suite
```

---

## 🚀 How to Run the Application

### 1. Open Terminal or PowerShell
Navigate to the project directory:
```powershell
cd C:\Users\YASH\.gemini\antigravity\scratch\ai_upskilling_platform
```

### 2. Run the Unit Tests (Optional Verification)
```powershell
python tests/test_pipeline.py
```
*(All 5 test suites will run and report `OK`)*

### 3. Launch the Web Interface
Double-click `run_app.bat` or run:
```powershell
python -m streamlit run app.py
```
The application will automatically launch in your browser at `http://localhost:8501`.

---

## 🎯 Review 2 Demonstration Walkthrough

When presenting to your project review panel:
1. **Choose a Pre-loaded Candidate Profile:**
   - In the sidebar, select **"⚡ Choose Sample Resume"** -> **"Alex Chen — Aspiring ML Engineer"**.
   - Show how the parser instantly extracts Alex's contact details, UC Berkeley degree, and identifies skills: Python, PyTorch, Scikit-Learn, Pandas, OpenCV, Git, etc.
2. **Select Target Role:**
   - Select **"Machine Learning Engineer"**.
3. **Show Extracted Profile (Tab 1):**
   - Demonstrate the domain categorization (Programming, ML & AI, Data Analysis, Software Engineering Tools).
   - Point out the estimated proficiency badges (*Advanced*, *Intermediate*, *Beginner*).
4. **Show Role Benchmark (Tab 2):**
   - Explain how each role has defined competencies with importance weights (`Critical = 3.0`, `High = 2.0`, `Medium = 1.0`).
5. **Show Skill Gap & Readiness Analytics (Tab 3):**
   - Point out the **Readiness Score** (e.g., 68.3% - Nearly Ready).
   - Show the **Radar Chart** comparing Candidate's current profile vs Role Benchmark.
   - Show the **Proficiency Gap Severity Chart** highlighting missing production competencies: **Docker**, **MLOps**, and **FastAPI**.
6. **Show Personalized Upskilling Roadmap (Tab 4):**
   - Point out how the system organizes learning into 3 sequential phases:
     - *Phase 1:* Bridge Critical Gaps (Docker, MLOps)
     - *Phase 2:* Core Frameworks (FastAPI API deployment)
     - *Phase 3:* Production tooling & portfolio projects
   - Show specific courses, project briefs, and practice assessment drills.
7. **Demonstrate AI Career Mentor (Tab 5):**
   - Click one of the quick questions (e.g. *"Why is Docker important for an ML Engineer?"*).
   - Show how the AI explains the exact business and technical justification for why an ML engineer must know containerization in production.
8. **Export Diagnostic Report (Tab 6):**
   - Download the generated evaluation markdown report as proof of deliverable.

---

## 💡 Viva / Q&A Preparation for Review 2

1. **Q: How does the system handle different resume formats?**
   - *A:* We built a multi-format ingestion module using `pypdf` for vector/standard PDFs, `python-docx` for MS Word documents, and UTF-8 decoders for plain text. It performs regex-based entity extraction and heuristic section segmentation.
2. **Q: How do you normalize different terms for the same skill?**
   - *A:* We built a hierarchical skill taxonomy (`data/skills_taxonomy.json`) storing canonical terms and aliases (e.g., `"py"`, `"python3"`, `"python programming"` all map to canonical `"Python"`). Multi-word terms are matched first to prevent partial substring collision.
3. **Q: How is the Role Readiness Score computed?**
   - *A:* It uses a weighted competency formulation:
     $$\text{Readiness Score} = \frac{\sum_{i=1}^N w_i \times \min\left(1.0, \frac{\text{Proficiency}_{\text{candidate}}}{\text{Proficiency}_{\text{expected}}}\right)}{\sum_{i=1}^N w_i} \times 100$$
     where critical competencies carry higher weights ($w = 3.0$) than general tools ($w = 1.0$).
4. **Q: What is planned for the next review (Review 3 / Phase 5-7)?**
   - *A:* Implementing interactive coding & MCQ assessments to dynamically test skills, fine-tuning LLM/RAG integration for personalized tutoring, and integrating database persistence.
