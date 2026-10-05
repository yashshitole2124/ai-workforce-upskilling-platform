"""
Role Competency Engine Module
Manages target job roles, expected skills, proficiency benchmarks, and role metadata.
"""

import os
import json
from typing import Dict, Any, List, Optional

class RoleEngine:
    def __init__(self, roles_path: str = None):
        if roles_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            roles_path = os.path.join(base_dir, "data", "role_competencies.json")

        self.roles_path = roles_path
        self.roles = self._load_roles()

    def _load_roles(self) -> Dict[str, Any]:
        with open(self.roles_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {r["role_id"]: r for r in data.get("roles", [])}

    def get_all_roles(self) -> List[Dict[str, Any]]:
        """
        Return list of all available roles with basic summary info.
        """
        return [
            {
                "role_id": r["role_id"],
                "role_title": r["role_title"],
                "domain": r["domain"],
                "description": r["description"],
                "competency_count": len(r.get("expected_competencies", []))
            }
            for r in self.roles.values()
        ]

    def get_role_by_id(self, role_id: str) -> Optional[Dict[str, Any]]:
        """
        Return full role profile by ID.
        """
        return self.roles.get(role_id)

    def get_role_competencies(self, role_id: str) -> List[Dict[str, Any]]:
        """
        Return expected competencies list for a given role.
        """
        role = self.get_role_by_id(role_id)
        if not role:
            return []
        return role.get("expected_competencies", [])
