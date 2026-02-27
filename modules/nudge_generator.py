import requests

def generate_nudge(total_spend, limit, addiction_score):

    prompt = f"""
    User spent ₹{total_spend}.
    Budget limit is ₹{limit}.
    Addiction score is {addiction_score}.

    Give a short funny financial nudge.
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]