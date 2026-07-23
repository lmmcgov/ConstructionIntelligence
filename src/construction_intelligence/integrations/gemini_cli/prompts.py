"""
Prompt templates for Gemini CLI evaluation.
"""

from construction_intelligence.core.evidence import Evidence
from construction_intelligence.core.project import Project


class GeminiPromptBuilder:
    """
    Builds structured prompts for Gemini.
    """

    def build_evidence_match_prompt(
        self,
        project: Project,
        evidence: Evidence,
    ) -> str:

        return f"""
You are evaluating whether external evidence confirms
an OpenStreetMap construction project.

Project:

Name:
{project.name}

City:
{project.city}

Road:
{project.road_name}


Evidence:

Title:
{evidence.title}

Content:
{evidence.content}

URL:
{evidence.url}


Return ONLY valid JSON.

Schema:

{{
  "match_score": 0.0,
  "status": "confirmed|likely|uncertain|rejected",
  "reasons": [],
  "resources": [
    {{
      "url": "",
      "title": "",
      "source": "",
      "resource_type": "",
      "excerpt": ""
    }}
  ]
}}
"""