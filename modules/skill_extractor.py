"""
Skill Extractor & Normalizer Module
Extracts technical competencies from resume text, maps synonyms to canonical taxonomy entries,
and estimates candidate proficiency levels.
"""

import os
import json
import re
from typing import Dict, Any, List, Set

class SkillExtractor:
    def __init__(self, taxonomy_path: str = None):
        if taxonomy_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            taxonomy_path = os.path.join(base_dir, "data", "skills_taxonomy.json")

        self.taxonomy_path = taxonomy_path
        self.taxonomy = self._load_taxonomy()
        self._build_lookup_index()

    def _load_taxonomy(self) -> Dict[str, Any]:
        with open(self.taxonomy_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _build_lookup_index(self):
        """
        Build alias to canonical skill mapping.
        Sort aliases by length descending so longer multi-word phrases match before substrings.
        """
        self.alias_to_skill = {}
        all_terms = []

        for skill in self.taxonomy.get("skills", []):
            skill_id = skill["id"]
            canonical = skill["canonical_name"]
            category = skill["category"]

            # Add canonical name
            canonical_clean = canonical.lower()
            self.alias_to_skill[canonical_clean] = skill
            all_terms.append((canonical_clean, skill))

            # Add id
            id_clean = skill_id.lower().replace("_", " ")
            self.alias_to_skill[id_clean] = skill
            all_terms.append((id_clean, skill))

            # Add aliases
            for alias in skill.get("aliases", []):
                alias_clean = alias.lower()
                self.alias_to_skill[alias_clean] = skill
                all_terms.append((alias_clean, skill))

        # Sort terms by length in descending order to match multi-word phrases first
        self.sorted_terms = sorted(all_terms, key=lambda x: len(x[0]), reverse=True)

    def _estimate_proficiency(self, skill_name: str, text: str, occurrences: int) -> str:
        """
        Heuristic to estimate proficiency (Beginner, Intermediate, Advanced) based on:
        - Frequency of occurrence across resume
        - Surrounding context adjectives and experience markers
        """
        lower_text = text.lower()
        
        # Look for explicit year mentions or seniority keywords near the skill
        advanced_cues = ["expert", "lead", "advanced", "architect", "5+ years", "4+ years", "3+ years", "extensive", "senior"]
        intermediate_cues = ["proficient", "experienced", "intermediate", "2 years", "1 year", "developed", "built", "implemented"]
        
        # Find context sentences around the skill
        sentences = re.split(r"[.\n;•]", lower_text)
        skill_lower = skill_name.lower()
        context_sentences = [s for s in sentences if skill_lower in s]

        has_advanced_cue = any(
            any(cue in s for cue in advanced_cues)
            for s in context_sentences
        )
        has_interm_cue = any(
            any(cue in s for cue in intermediate_cues)
            for s in context_sentences
        )

        if has_advanced_cue or occurrences >= 4:
            return "Advanced"
        elif has_interm_cue or occurrences >= 2:
            return "Intermediate"
        else:
            return "Beginner"

    def extract_skills(self, text: str) -> Dict[str, Any]:
        """
        Extract normalized skills from text.
        Returns extracted skills, estimated proficiency, categories, and evidence sentences.
        """
        text_lower = text.lower()
        # Clean special chars but preserve spaces and hyphens
        normalized_text = re.sub(r"[^\w\s\+\#\.\-]", " ", text_lower)

        found_skills = {}
        matched_spans = set()

        for term, skill_meta in self.sorted_terms:
            skill_id = skill_meta["id"]
            if skill_id in found_skills:
                continue

            # Special case for C++, C#, R, Go to ensure precise boundaries
            if term in ["c++", "c/c++"]:
                pattern = r"(?:\b|(?<=\s))c\+\+(?:\b|(?=\s))"
            elif term in ["c#", "c-sharp"]:
                pattern = r"(?:\b|(?<=\s))c\#(?:\b|(?=\s))"
            elif term == "r":
                pattern = r"(?:\b|(?<=\s))r(?:\b|(?=\s))(?:\s+programming|\s+language|\s+script)?"
            elif term == "go":
                pattern = r"\b(?:golang|go language)\b"
            else:
                escaped_term = re.escape(term)
                pattern = r"\b" + escaped_term + r"\b"

            matches = list(re.finditer(pattern, normalized_text))
            if matches:
                occurrences = len(matches)
                proficiency = self._estimate_proficiency(skill_meta["canonical_name"], text, occurrences)
                
                # Extract up to 2 context snippet sentences
                sentences = re.split(r"[.\n•]", text)
                snippets = [
                    s.strip() for s in sentences 
                    if re.search(r"\b" + re.escape(term) + r"\b", s, re.IGNORECASE) and len(s.strip()) > 10
                ][:2]

                found_skills[skill_id] = {
                    "id": skill_id,
                    "canonical_name": skill_meta["canonical_name"],
                    "category": skill_meta["category"],
                    "estimated_proficiency": proficiency,
                    "frequency": occurrences,
                    "context_snippets": snippets
                }

        # Group by category
        by_category = {}
        for skill_id, data in found_skills.items():
            cat = data["category"]
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(data)

        # Proficiency counts
        prof_counts = {"Beginner": 0, "Intermediate": 0, "Advanced": 0}
        for data in found_skills.values():
            p = data["estimated_proficiency"]
            prof_counts[p] = prof_counts.get(p, 0) + 1

        return {
            "total_extracted": len(found_skills),
            "skills": found_skills,
            "skills_by_category": by_category,
            "proficiency_distribution": prof_counts
        }
