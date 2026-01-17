import json
from langchain_google_genai import ChatGoogleGenerativeAI

class FactChecker:
    def __init__(self, api_key: str):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,  # deterministic for fact-checking
            api_key=api_key  # pass the API key here if supported
        )

    def verify_claim(self, claim: str, web_context: str) -> dict:
        prompt = f"""
You are a professional fact-checker.

Claim:
"{claim}"

Live web information:
"{web_context}"

Instructions:
- Classify the claim strictly as one of: VERIFIED, INACCURATE, FALSE
- Use ONLY the provided web information
- Do NOT hallucinate facts
- Return ONLY valid JSON

JSON format:
{{
  "status": "VERIFIED | INACCURATE | FALSE",
  "explanation": "short justification",
  "corrected_fact": "correct info if applicable, else empty string"
}}
"""

        response = self.llm.invoke(prompt)
        content = response.content.strip()

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            import re
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
