import requests

def tavily_search(query: str, api_key: str) -> dict:
    if not api_key:
        raise ValueError("TAVILY_API_KEY not set")

    url = "https://api.tavily.com/search"
    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "advanced",
        "include_answer": True
    }
    response = requests.post(url, json=payload, timeout=20)
    response.raise_for_status()
    return response.json()
