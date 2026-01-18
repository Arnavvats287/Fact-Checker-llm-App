import json
import re
from langchain_google_genai import ChatGoogleGenerativeAI

class FactChecker:
    def __init__(self, api_key: str):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            api_key=api_key
        )

    def verify_claim(self, claim: str, web_context: str) -> dict:
        prompt = f"""
You are a STRICT professional fact-checker.

Claim:
"{claim}"

Web evidence:
"{web_context}"

Decision rules (VERY IMPORTANT):
- VERIFIED → Only if the claim is explicitly confirmed as factual by reliable sources
- INACCURATE → If the claim is partially true, outdated, speculative, or imprecise
- FALSE → If the claim is contradicted, unsupported, or refers to an event that has not occurred

Additional constraints:
- Predictions, opinions, forecasts, or rumors are NEVER VERIFIED
- Future events are NEVER VERIFIED
- If evidence is mixed or unclear → INACCURATE
- Be conservative: prefer INACCURATE over VERIFIED
- Use ONLY the provided web evidence
- Do NOT add external knowledge
- Do NOT hallucinate

Return ONLY valid JSON in the following format:

{{
  "status": "VERIFIED | INACCURATE | FALSE",
  "explanation": "1–2 sentence justification",
  "corrected_fact": "Corrected version if INACCURATE or FALSE, else empty string"
}}
"""

        response = self.llm.invoke(prompt)
        content = response.content.strip()

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Fallback: extract JSON if model wraps it in text
            match = re.search(r"\{.*\}", content, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except json.JSONDecodeError:
                    pass

            return {
                "status": "ERROR",
                "explanation": content,
                "corrected_fact": ""
            }
