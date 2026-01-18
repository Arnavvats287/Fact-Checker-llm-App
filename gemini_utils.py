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

Classification definitions:
- VERIFIED:
  The claim is explicitly confirmed by the provided evidence.
  This INCLUDES future events if the claim correctly states they are scheduled or planned.

- INACCURATE:
  The claim is partially correct but contains errors such as:
  • wrong date or year
  • outdated statistics
  • overstating certainty
  • claiming completion when evidence says scheduled
  • forecasts or predictions treated as facts
  • mixed or unclear evidence

- FALSE:
  The claim is directly contradicted by evidence
  OR has no supporting evidence
  OR claims an event already happened when it has not occurred.

Important constraints:
- Future events are NOT automatically false
- Future events are VERIFIED only if explicitly described as scheduled/planned
- Predictions, opinions, and speculation are NEVER VERIFIED
- If unsure → choose INACCURATE
- Be conservative: prefer INACCURATE over VERIFIED
- Use ONLY the provided web evidence
- Do NOT add external knowledge
- Do NOT hallucinate

Return ONLY valid JSON in this format:

{{
  "status": "VERIFIED | INACCURATE | FALSE",
  "explanation": "1–2 sentence justification",
  "corrected_fact": "Corrected version if INACCURATE or FALSE, else empty string"
}}
"""

        response = self.llm.invoke(prompt)
        content = response.content.strip()

        # Attempt direct JSON parse
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            pass

        # Fallback: extract JSON safely
        match = re.search(r"\{[\s\S]*\}", content)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass

        # Absolute fallback (never crash app)
        return {
            "status": "ERROR",
            "explanation": content,
            "corrected_fact": ""
        }
