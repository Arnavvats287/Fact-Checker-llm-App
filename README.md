<div align="center">

# 😎 Fact-Checking Web App
### Verify your claims with this ai app

</div>

---

🎥 **Demo Video:**  
👉 *[PASTE YOUR DEMO VIDEO LINK HERE]*

🌐 **Live App url:**  
👉 *https://fact-llm-checker-arnav.streamlit.app/*

---

## Project Overview

This project is an **AI-powered fact-checking web application** that automatically extracts factual claims from uploaded pdf documents and verifies them against **live web data**.

It is designed to detect:
- ❌ **False claims**
- ⚠️ **Inaccurate information**
- ✅ **Verified facts**

---

## How to Run the Project locally ~

### 1. clone/download the project

Place the project folder on your pc.

### 2. create and activate a Virtual Environment

```bash
python -m venv venv
venv\\Scripts\\activate  
```

### 3. install the requirements

```bash
pip install -r requirements.txt
```

### 4. set Environment Variables

Create a `.env` file in the root directory:

```
GOOGLE_API_KEY=your_api_key
TRAVILY_KEY=your_api_key
```

### 5. run the streamlit apllication in terminal

```bash
streamlit run app.py
```

### 6. app will run at :

```arduino
http://localhost:----
```

---

## architecture overview

### Flow of app

```text
PDF Upload
   ↓
Claim Extraction (PDF Parsing / pdfpumber)
   ↓
Live Web Search (Tavily api)
   ↓
LLM Verification (Gemini api via Langchain)
   ↓
Structured Results Table (Streamlit ui)
```

## Requirements

project requires the following dependencues:
 
* Python 3.9+
* Streamlit
* Langchain
* Google Gemini API
* Tavily search API
* python-dotenv
* pdfplumber
* requests

All are listed in `requirements.txt`, just run the file.

## How the App Works

### 1. PDF Upload

Users upload a document which has the claims.

### 2. Claim Extraction

The system identifies verifiable claims including:

* Dates

* Statistics

* Financial figures

* Technical details

### 3. Live Web Search

Each claim is searched through real web data /evidence using Tavily to retrive for the llm

### 4. AI Fact verification

The LLM applies strict rules:

```VERIFIED``` → actually confirmed

```INACCURATE``` → partially true or outdated

```FALSE``` → Contradicted or incorrect

Predictions, rumors, and speculation are never VERIFIED

### 5. Results Display

Results show sequentially and then the final output table is made which includes:

* Claim

* Status

* Explanation

* Corrected Fact

* Sources

## Demo Claims Used for Evaluation
( chatgpt was used for getting demo claims)

Example claims tested:

1. “Bitcoin reached an all-time high of $100,000 in December 2025.”

2. “Unemployment has risen to 6.2%, forcing the Federal Reserve to consider emergency rate cuts.”

3) “The Artemis III moon landing mission was successfully completed in 2025.”

4) “Real GDP growth for 2025 was -1.5%.”

These were intentionally mixed with false, outdated, and misleading claims.

## Application Screenshots

### Streamlit Home Page

![Streamlit Home Page](Screenshots/home.png "Streamlit UI")

### claims extraction page

![Streamlit Home Page](Screenshots/json.png "Streamlit UI")

### Final output table

![Streamlit Home Page](Screenshots/retrieved.png "Streamlit UI")

---

## Conclusion

this app combines the use of llm in accordance to live web search data to deliver a practical and transparent fact checker. by verifying claims through derived rules and clearly explaining each verdict with peroper proofs/sources, it helps users identify false, inaccurate, and outdated information in documents. The app is deployed with a clean drag and drop feature for the pdf and the app is easy to use, accessible and ready for real-world data.

<div align="center">
Thanks, made with 💜 by arnav

</div>



