"""
AI Mentor Module
Provides conversational guidance, contextual explanations of skill gaps,
and structured career mentoring grounded in the candidate's analysis.
"""

from typing import Dict, Any, List

class AIMentor:
    def __init__(self):
        # Knowledge bank for explainable gap reasons
        self.role_insights = {
            "ml_engineer": {
                "docker": "In production, ML models cannot just run on local Jupyter notebooks. Companies require containerization with Docker to ensure reproducible dependencies, zero environment drift, and seamless Kubernetes deployment.",
                "fastapi": "Data science models need to be served via high-throughput, low-latency REST endpoints. FastAPI provides native async support, Pydantic data validation, and automated OpenAPI documentation.",
                "mlops": "Over 80% of ML models fail to make it to production without MLOps. Automated CI/CD, experiment tracking (MLflow), and model registry are essential to detect data drift and automate retraining.",
                "sql": "Feature engineering starts with raw data stored in relational or data warehouse systems. Efficient SQL querying reduces preprocessing bottlenecks.",
                "aws": "Cloud providers like AWS provide scalable GPU compute (EC2), managed model hosting (SageMaker), and S3 storage critical for enterprise AI workloads."
            },
            "data_analyst": {
                "sql": "SQL is the single most important skill for a data analyst. Analysts must comfortably write CTEs, window functions (ROW_NUMBER, LAG, LEAD), and complex aggregations.",
                "tableau": "Business executives rarely read raw tables. Interactive dashboards with drill-downs in Tableau or Power BI allow non-technical decision makers to explore trends.",
                "statistics": "A/B testing, hypothesis testing, and confidence intervals prevent drawing false conclusions from business data correlations."
            },
            "software_developer": {
                "rest_api": "Modern software architectures are decoupled. Building reliable REST APIs with standard HTTP status codes, pagination, and error handling is fundamental.",
                "docker": "Docker allows software developers to replicate production database and microservice configurations locally with zero installation conflicts.",
                "data_structures": "Efficient algorithmic problem solving directly impacts system latency, memory usage, and backend throughput."
            }
        }

    def generate_mentor_briefing(self, candidate_name: str, role_title: str, gap_data: Dict[str, Any]) -> str:
        """
        Generate a personalized executive mentoring summary for the learner.
        """
        score = gap_data.get("readiness_score", 0.0)
        tier = gap_data.get("readiness_tier", "")
        matches = gap_data.get("matches", [])
        missing = gap_data.get("missing_skills", [])
        partial = gap_data.get("partial_matches", [])

        name_display = candidate_name if candidate_name != "Not Detected" else "Learner"

        briefing = []
        briefing.append(f"### 🤖 AI Mentor Career Diagnostic for **{name_display}**")
        briefing.append(f"**Target Role:** {role_title} | **Current Readiness Score:** `{score}%` ({tier})\n")

        # Strengths summary
        if matches:
            top_strengths = [m["canonical_name"] for m in matches[:4]]
            briefing.append(f"🌟 **Core Strengths Identified:** You have strong alignment in **{', '.join(top_strengths)}**. This provides a formidable base to build upon.")
        else:
            briefing.append("🌟 **Foundations:** You have initiated your upskilling journey. Prioritizing core fundamentals will yield the highest return.")

        # Key gaps
        critical_missing = [m["canonical_name"] for m in missing if m.get("importance") == "Critical"]
        high_missing = [m["canonical_name"] for m in missing if m.get("importance") == "High"]

        if critical_missing:
            briefing.append(f"\n⚠️ **Top Priority Bottlenecks:** To pass screening for **{role_title}**, you must immediately address: **{', '.join(critical_missing)}**. In industry hiring assessments, missing these competencies often triggers automatic filter rejection.")
        elif high_missing:
            briefing.append(f"\n⚠️ **Recommended Focus:** You are missing **{', '.join(high_missing)}**, which are key differentiators during technical interviews.")

        # Partial improvements
        if partial:
            upgrades = [f"{p['canonical_name']} ({p['candidate_proficiency']} → {p['expected_proficiency']})" for p in partial[:3]]
            briefing.append(f"\n📈 **Proficiency Upgrades:** Elevating existing skills **{', '.join(upgrades)}** through hands-on project implementations will rapidly lift your readiness score.")

        briefing.append(f"\n💡 **Next Step Advice:** Follow Phase 1 of your personalized roadmap below. Allocate 8-10 hours per week focusing on practical project implementation rather than passive video consumption.")

        return "\n".join(briefing)

    def answer_question(self, question: str, role_id: str, gap_data: Dict[str, Any]) -> str:
        """
        Answer learner questions with contextual relevance to their target role and gaps.
        """
        q_lower = question.lower()
        role_map = self.role_insights.get(role_id, {})

        # Check for specific skill explanation
        for skill_key, explanation in role_map.items():
            if skill_key in q_lower:
                return (
                    f"**Why {skill_key.upper()} is crucial for this role:**\n\n"
                    f"{explanation}\n\n"
                    f"👉 **Mentor Recommendation:** Add a small production-ready micro-project showcasing this skill to your portfolio. Check the Roadmap tab for recommended courses and project specifications."
                )

        if "how long" in q_lower or "duration" in q_lower or "time" in q_lower:
            score = gap_data.get("readiness_score", 50)
            weeks = max(4, int((100 - score) / 10) * 2)
            return (
                f"Based on your current readiness score of **{score}%**, dedicating **8 to 10 focused hours per week** will allow you to bridge your primary critical gaps in approximately **{weeks} to {weeks + 3} weeks**.\n\n"
                f"Consistency in building practical code artifacts is far more effective than marathon reading sessions!"
            )

        if "project" in q_lower or "portfolio" in q_lower:
            missing = [m["canonical_name"] for m in gap_data.get("missing_skills", [])[:2]]
            missing_str = " and ".join(missing) if missing else "cloud deployment"
            return (
                f"For your target role, the best project you can build right now is an **End-to-End Application** combining your existing strengths with your missing skills (**{missing_str}**).\n\n"
                f"For example, rather than an isolated script, build a full pipeline with automated tests, containerize it with Docker, write a clear README, and deploy it to a cloud service (AWS/Render) with a public demo URL."
            )

        if "interview" in q_lower or "resume" in q_lower:
            return (
                "**Interview Readiness Tip:**\n\n"
                "1. Highlight quantitative impact in your bullet points (e.g., 'Optimized pipeline runtime by 35%').\n"
                "2. Be ready to explain trade-offs: Why did you pick a certain algorithm or framework over alternatives?\n"
                "3. Ensure every skill listed on your resume is backed by at least one demonstrable project."
            )

        # Default intelligent response
        return (
            f"As your AI Career Mentor for this upskilling pathway, my priority is keeping you focused on the highest-leverage skills.\n\n"
            f"Your current readiness score is **{gap_data.get('readiness_score')}%**. Take a look at the **Skill Gap** and **Roadmap** tabs to see the exact sequence of courses and hands-on milestones calibrated for your profile."
        )
