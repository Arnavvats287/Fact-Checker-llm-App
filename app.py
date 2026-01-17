import streamlit as st

from pdf_utils import extract_claims_from_pdf
from search_utils import tavily_search
from gemini_utils import FactChecker

st.set_page_config(page_title="AI Fact Checker", layout="wide")

st.title("📄 AI Fact-Checking Web App")
st.caption("Verify factual claims in PDFs using LangChain + Gemini + live web data.")

# Get API keys from Streamlit secrets
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    claims = extract_claims_from_pdf(uploaded_file)
    st.write(f"Extracted claims ({len(claims)}):")
    st.write(claims)

    if not claims:
        st.warning("No factual claims detected.")
        st.stop()

    if st.button("Check Claims"):
        fact_checker = FactChecker(api_key=GEMINI_API_KEY)  # pass key if your class supports it
        results = []

        result_placeholder = st.empty()

        for idx, claim in enumerate(claims):
            with st.spinner(f"Verifying claim {idx + 1} of {len(claims)}..."):
                try:
                    search_results = tavily_search(claim, api_key=TAVILY_API_KEY)  # pass key if needed
                    web_context = search_results.get("answer", "")
                    verdict = fact_checker.verify_claim(claim, web_context)
                except Exception as e:
                    verdict = {
                        "status": "ERROR",
                        "explanation": str(e),
                        "corrected_fact": ""
                    }

                results.append({
                    "Claim": claim,
                    "Status": verdict.get("status"),
                    "Explanation": verdict.get("explanation"),
                    "Corrected Fact": verdict.get("corrected_fact"),
                    "Sources": ", ".join(
                        r.get("url", "") for r in search_results.get("results", [])[:3]
                    ) if search_results else ""
                })

                result_placeholder.dataframe(results, use_container_width=True)

        st.success("Fact-checking complete!")

st.markdown("---")
st.markdown(
    "Made with by **Arnav** ~ "
)

