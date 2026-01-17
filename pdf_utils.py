import pdfplumber
import re
from typing import List

def extract_claims_from_pdf(file) -> List[str]:
    """
    Extract sentences likely to contain factual claims.
    """
    claims = []

    with pdfplumber.open(file) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)

    sentences = re.split(r'(?<=[.!?])\s+', text)

    for sentence in sentences:
        if re.search(r'(\$|%|\d{4}|\d+\.\d+)', sentence):
            claims.append(sentence.strip())

    return list(set(claims))
