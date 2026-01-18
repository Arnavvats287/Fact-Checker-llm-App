import json
import re
from langchain_google_genai import ChatGoogleGenerativeAI
import os


class FactChecker:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0
        )

    def verify_claim(self, claim: str, web_context: str) -> dict:
        """
        Verify a factual claim using live web context.
        Handles:
        - Past vs future events
        - Scheduled vs completed events
        - Date mismatches
        - Outdated or incorrect statistics
        """

        prompt = f"""
You are a professional fact-checker.

Claim:
"{claim}"

Live web information:
"{web_context}"

Rules (IMPORTANT):
- Use ONLY the provided web information
- Do NOT assume events happened unless explicitly stated
- If a claim states an event already happened, but evidence says it is scheduled or delayed → INACCURATE
- If a claim states something happened on the wrong date → INACCURATE
- If there is no supporting evidence at all → FALSE
- Future-scheduled events can be VERIFIED ONLY if the claim correctly states they are scheduled/planned
- Do NOT mark something FALSE only because it is future, unless the claim says it already happened

Classification options (STRICT):
- VERIFIED
- INACCURATE
- FALSE

Return ONLY valid JSON in this exact format:

{{
  "status": "VERIFIED | INACCURATE | FALSE",
  "explanation": "concise factual justification",
  "corrected_fact": "correct information if applicable, otherwise empty string"
}}
"""

        response = self.llm.invoke(prompt)
        content = response.content.strip()

        # First attempt: direct JSON
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            pass

        # Fallback: extract JSON block safely
        match = re.search(r"\{[\s\S]*\}", content)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass

        # Final fallback (never crash Streamlit)
        return {
            "status": "ERROR",
            "explanation": content,
            "corrected_fact": ""
        }
