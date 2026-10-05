"""
Recommendation Engine Module
Generates personalized learning paths, courses, project recommendations,
and milestones based on identified skill gaps.
"""

import os
import json
from typing import Dict, Any, List

class Recommender:
    def __init__(self, resources_path: str = None):
        if resources_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            resources_path = os.path.join(base_dir, "data", "learning_resources.json")

        self.resources_path = resources_path
        self.resources = self._load_resources()

    def _load_resources(self) -> Dict[str, Any]:
        with open(self.resources_path, "r", encoding="utf-8") as f:
            return json.load(f).get("resources", {})

    def generate_roadmap(self, gap_results: Dict[str, Any], role_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a multi-phase personalized upskilling roadmap.
        """
        prioritized_gaps = gap_results.get("prioritized_gaps", [])
        
        # Categorize gaps into phases
        phase1_critical = [g for g in prioritized_gaps if "Critical" in g["priority_label"]]
        phase2_high = [g for g in prioritized_gaps if "High" in g["priority_label"]]
        phase3_medium = [g for g in prioritized_gaps if "Medium" in g["priority_label"]]

        phases = []

        if phase1_critical:
            phase1_items = []
            for item in phase1_critical:
                res = self.resources.get(item["skill_id"], {})
                phase1_items.append({
                    "skill": item["skill_name"],
                    "gap_type": item["gap_type"],
                    "target_level": item["target_level"],
                    "courses": res.get("courses", [{"title": f"Mastering {item['skill_name']}", "provider": "Standard Curriculum", "level": item["target_level"], "type": "Course", "duration": "3 weeks"}]),
                    "projects": res.get("projects", [f"Implement an end-to-end microservice utilizing {item['skill_name']}."]),
                    "practice": res.get("practice", f"Solve foundational and intermediate coding exercises in {item['skill_name']}.")
                })
            phases.append({
                "phase_number": 1,
                "title": "Phase 1: Bridge Critical Foundational Gaps",
                "focus": "Immediate prerequisite competencies required for the target role",
                "estimated_time": "3 - 5 Weeks",
                "items": phase1_items
            })

        if phase2_high:
            phase2_items = []
            for item in phase2_high:
                res = self.resources.get(item["skill_id"], {})
                phase2_items.append({
                    "skill": item["skill_name"],
                    "gap_type": item["gap_type"],
                    "target_level": item["target_level"],
                    "courses": res.get("courses", [{"title": f"Applied {item['skill_name']} for Engineers", "provider": "Professional Certification", "level": item["target_level"], "type": "Course", "duration": "3 weeks"}]),
                    "projects": res.get("projects", [f"Build a production-grade component showcasing {item['skill_name']}."]),
                    "practice": res.get("practice", f"Practice building real-world workflows in {item['skill_name']}.")
                })
            phases.append({
                "phase_number": 2,
                "title": "Phase 2: Strengthen Core Role Competencies",
                "focus": "High-impact technical proficiencies and framework mastery",
                "estimated_time": "3 - 4 Weeks",
                "items": phase2_items
            })

        if phase3_medium or not phases:
            phase3_items = []
            target_list = phase3_medium if phase3_medium else prioritized_gaps
            for item in target_list:
                res = self.resources.get(item["skill_id"], {})
                phase3_items.append({
                    "skill": item["skill_name"],
                    "gap_type": item["gap_type"],
                    "target_level": item["target_level"],
                    "courses": res.get("courses", []),
                    "projects": res.get("projects", []),
                    "practice": res.get("practice", "Refine code architecture and adhere to industry style guidelines.")
                })
            phases.append({
                "phase_number": len(phases) + 1,
                "title": f"Phase {len(phases) + 1}: Tooling, Architecture & Portfolio Polishing",
                "focus": "Production deployment, CI/CD, testing, and interview project readiness",
                "estimated_time": "2 - 3 Weeks",
                "items": phase3_items
            })

        total_courses = sum(len(i["courses"]) for p in phases for i in p["items"])
        total_projects = sum(len(i["projects"]) for p in phases for i in p["items"])

        return {
            "target_role": role_data.get("role_title", "Target Role"),
            "phases": phases,
            "summary": {
                "total_phases": len(phases),
                "total_gaps_addressed": len(prioritized_gaps),
                "total_recommended_courses": total_courses,
                "total_recommended_projects": total_projects,
                "estimated_completion_time": f"{len(phases) * 3}-{len(phases) * 4} Weeks (at 8-10 hrs/week)"
            }
        }
