"""
Resume Parser Module
Extracts plain text and structured metadata (contact info, education, experience, sections)
from PDF, DOCX, and TXT resume files.
"""

import os
import re
from typing import Dict, Any, List, Optional
import pypdf
import docx

class ResumeParser:
    def __init__(self):
        # Common section header keywords
        self.section_patterns = {
            "summary": re.compile(r"^(summary|professional summary|profile|about me|objective)", re.IGNORECASE),
            "education": re.compile(r"^(education|academic background|academics|qualifications)", re.IGNORECASE),
            "experience": re.compile(r"^(experience|work experience|employment history|professional experience|internships)", re.IGNORECASE),
            "projects": re.compile(r"^(projects|key projects|academic projects|technical projects)", re.IGNORECASE),
            "skills": re.compile(r"^(skills|technical skills|core competencies|areas of expertise|technologies)", re.IGNORECASE),
            "certifications": re.compile(r"^(certifications|licenses|courses|certificates)", re.IGNORECASE),
        }

    def extract_text_from_file(self, file_path_or_bytes, filename: str = "") -> str:
        """
        Extract text from file path or file-like object (bytes) based on extension.
        """
        ext = os.path.splitext(filename)[1].lower() if filename else ""

        # If it's a file path or direct string
        if isinstance(file_path_or_bytes, str):
            if os.path.isfile(file_path_or_bytes):
                if not ext:
                    ext = os.path.splitext(file_path_or_bytes)[1].lower()
                if ext == ".pdf":
                    return self._extract_from_pdf(file_path_or_bytes)
                elif ext in [".docx", ".doc"]:
                    return self._extract_from_docx(file_path_or_bytes)
                else:
                    with open(file_path_or_bytes, "r", encoding="utf-8", errors="ignore") as f:
                        return f.read()
            else:
                # Direct string content
                return file_path_or_bytes

        # If it's a file-like object or bytes (e.g. from Streamlit UploadedFile)
        else:
            if ext == ".pdf":
                return self._extract_from_pdf_stream(file_path_or_bytes)
            elif ext in [".docx", ".doc"]:
                return self._extract_from_docx_stream(file_path_or_bytes)
            else:
                try:
                    return file_path_or_bytes.read().decode("utf-8", errors="ignore")
                except Exception:
                    file_path_or_bytes.seek(0)
                    return str(file_path_or_bytes.read())

    def _extract_from_pdf(self, file_path: str) -> str:
        text = []
        try:
            reader = pypdf.PdfReader(file_path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
        except Exception as e:
            text.append(f"Error reading PDF: {str(e)}")
        return "\n".join(text)

    def _extract_from_pdf_stream(self, stream) -> str:
        text = []
        try:
            reader = pypdf.PdfReader(stream)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
        except Exception as e:
            text.append(f"Error reading PDF stream: {str(e)}")
        return "\n".join(text)

    def _extract_from_docx(self, file_path: str) -> str:
        text = []
        try:
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                if para.text.strip():
                    text.append(para.text.strip())
            for table in doc.tables:
                for row in table.rows:
                    row_text = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                    if row_text:
                        text.append(" | ".join(row_text))
        except Exception as e:
            text.append(f"Error reading DOCX: {str(e)}")
        return "\n".join(text)

    def _extract_from_docx_stream(self, stream) -> str:
        text = []
        try:
            doc = docx.Document(stream)
            for para in doc.paragraphs:
                if para.text.strip():
                    text.append(para.text.strip())
            for table in doc.tables:
                for row in table.rows:
                    row_text = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                    if row_text:
                        text.append(" | ".join(row_text))
        except Exception as e:
            text.append(f"Error reading DOCX stream: {str(e)}")
        return "\n".join(text)

    def clean_text(self, text: str) -> str:
        """
        Normalize whitespace and standard bullets.
        """
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        # Replace non-breaking spaces and unusual bullet characters
        text = re.sub(r"[\u2022\u2023\u25E6\u2043\u2219\uF0B7\uF0A7]", "•", text)
        # Normalize multiple spaces (preserving newlines)
        lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.split("\n")]
        return "\n".join(lines)

    def extract_contact_info(self, text: str) -> Dict[str, Any]:
        """
        Extract candidate name, email, phone number, and social links.
        """
        email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
        phone_pattern = r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
        linkedin_pattern = r"(?:https?:\/\/)?(?:www\.)?linkedin\.com\/in\/[a-zA-Z0-9_-]+"
        github_pattern = r"(?:https?:\/\/)?(?:www\.)?github\.com\/[a-zA-Z0-9_-]+"

        emails = re.findall(email_pattern, text)
        phones = re.findall(phone_pattern, text)
        linkedins = re.findall(linkedin_pattern, text, re.IGNORECASE)
        githubs = re.findall(github_pattern, text, re.IGNORECASE)

        # Name heuristic: inspect the first 5 non-empty lines
        name = "Not Detected"
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        for line in lines[:5]:
            # Skip if contains email, phone, url, or header words
            if re.search(r"[@|http|www|resume|curriculum|phone|email]", line, re.IGNORECASE):
                continue
            # Remove symbols
            candidate = re.sub(r"[^a-zA-Z\s]", "", line).strip()
            words = candidate.split()
            if 1 <= len(words) <= 4 and all(w[0].isupper() for w in words if len(w) > 1):
                name = candidate
                break

        return {
            "name": name,
            "email": emails[0] if emails else "Not Found",
            "phone": phones[0] if phones else "Not Found",
            "linkedin": linkedins[0] if linkedins else "Not Found",
            "github": githubs[0] if githubs else "Not Found",
        }

    def segment_sections(self, text: str) -> Dict[str, str]:
        """
        Segment resume into logical sections: summary, education, experience, projects, skills, certifications.
        """
        lines = text.split("\n")
        sections = {
            "header": "",
            "summary": "",
            "education": "",
            "experience": "",
            "projects": "",
            "skills": "",
            "certifications": "",
            "other": ""
        }

        current_section = "header"
        for line in lines:
            trimmed = line.strip()
            if not trimmed:
                continue

            # Check if this line looks like a header (short, matches section keywords)
            if len(trimmed.split()) <= 5:
                matched_sec = None
                for sec, pattern in self.section_patterns.items():
                    if pattern.search(trimmed):
                        matched_sec = sec
                        break
                if matched_sec:
                    current_section = matched_sec
                    continue

            sections[current_section] += trimmed + "\n"

        return sections

    def extract_education(self, text: str) -> List[str]:
        """
        Extract degrees and universities mentions.
        """
        edu_keywords = [
            r"B\.?Tech(?:nology)?", r"B\.?E\.?", r"M\.?Tech(?:nology)?", r"M\.?E\.?",
            r"B\.?S\.?(?:c)?", r"M\.?S\.?(?:c)?", r"Bachelor(?:'s)?", r"Master(?:'s)?",
            r"Ph\.?D\.?", r"MCA", r"BCA", r"Diploma", r"Degree"
        ]
        edu_entries = []
        lines = text.split("\n")
        for i, line in enumerate(lines):
            for kw in edu_keywords:
                if re.search(r"\b" + kw + r"\b", line, re.IGNORECASE):
                    entry = line.strip()
                    # Add next line if it mentions university or year
                    if i + 1 < len(lines) and len(lines[i+1].strip()) > 0 and len(lines[i+1].strip()) < 80:
                        entry += " — " + lines[i+1].strip()
                    if entry not in edu_entries:
                        edu_entries.append(entry)
                    break
        return edu_entries

    def parse(self, file_path_or_bytes, filename: str = "") -> Dict[str, Any]:
        """
        Full parse pipeline returning structured candidate data.
        """
        raw_text = self.extract_text_from_file(file_path_or_bytes, filename)
        cleaned_text = self.clean_text(raw_text)
        contact_info = self.extract_contact_info(cleaned_text)
        sections = self.segment_sections(cleaned_text)
        education_list = self.extract_education(sections.get("education", "") or cleaned_text)

        word_count = len(cleaned_text.split())
        char_count = len(cleaned_text)

        return {
            "contact_info": contact_info,
            "education": education_list,
            "sections": sections,
            "raw_text": cleaned_text,
            "stats": {
                "word_count": word_count,
                "char_count": char_count,
                "sections_found": [k for k, v in sections.items() if len(v.strip()) > 0 and k != "header"]
            }
        }
