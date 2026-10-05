"""
Career Analytics & Multi-Role Pathways Module
Analyzes candidate fit across multiple industry career paths simultaneously,
identifies highest-ROI skills to learn, and provides strategic transition advice.
"""

from typing import Dict, Any, List

class CareerAnalytics:
    def __init__(self, role_engine, gap_analyzer):
        self.role_engine = role_engine
        self.gap_analyzer = gap_analyzer

    def analyze_all_roles(self, extracted_skills: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate candidate readiness across every configured industry role.
        """
        all_roles = self.role_engine.get_all_roles()
        role_evaluations = []
        skill_impact_map = {}

        for role_meta in all_roles:
            role_id = role_meta["role_id"]
            full_role = self.role_engine.get_role_by_id(role_id)
            if not full_role:
                continue

            analysis = self.gap_analyzer.analyze_gap(extracted_skills, full_role)
            role_evaluations.append({
                "role_id": role_id,
                "role_title": full_role["role_title"],
                "domain": full_role.get("domain", ""),
                "readiness_score": analysis["readiness_score"],
                "readiness_tier": analysis["readiness_tier"],
                "matched_count": analysis["fully_matched_count"],
                "missing_count": analysis["missing_count"],
                "total_skills": analysis["total_role_skills"]
            })

            # Track which missing skills appear across multiple roles
            for missing in analysis.get("missing_skills", []):
                s_id = missing["skill_id"]
                s_name = missing["canonical_name"]
                if s_id not in skill_impact_map:
                    skill_impact_map[s_id] = {
                        "skill_name": s_name,
                        "roles_impacted": [],
                        "total_weight": 0.0
                    }
                skill_impact_map[s_id]["roles_impacted"].append(full_role["role_title"])
                skill_impact_map[s_id]["total_weight"] += missing.get("weight", 1.0)

        # Sort roles by readiness score descending
        role_evaluations.sort(key=lambda x: x["readiness_score"], reverse=True)

        # Rank highest ROI skills (skills appearing across the most roles with high weight)
        highest_roi_skills = sorted(
            skill_impact_map.values(),
            key=lambda x: (len(x["roles_impacted"]), x["total_weight"]),
            reverse=True
        )[:5]

        # Best alternative role
        best_match_role = role_evaluations[0] if role_evaluations else None

        return {
            "role_evaluations": role_evaluations,
            "best_match_role": best_match_role,
            "highest_roi_skills": highest_roi_skills
        }
