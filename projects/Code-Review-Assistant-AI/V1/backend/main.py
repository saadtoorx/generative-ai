from fastapi import FastAPI, Form
import requests

app = FastAPI()

@app.post("/review/")
def review_code(code: str = Form(...)):
    prompt = (
        "You are a senior developer. Please review the following code for bugs, "
        "improvements, and optimization tips:\n\n"
        f"{code}"
    )

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "deepseek-coder",
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()
    return {"review": result["response"].strip()}
