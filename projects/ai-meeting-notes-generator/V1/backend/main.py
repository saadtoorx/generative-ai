from fastapi import FastAPI, UploadFile, File
import whisper
import requests
import tempfile

app = FastAPI()

# Load Whisper model (use 'small' for better accuracy if needed)
model = whisper.load_model("base")

def call_ollama(prompt: str) -> str:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama2",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"].strip()

@app.post("/process/")
async def process_audio(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    transcript = model.transcribe(tmp_path)["text"]

    summary_prompt = (
        "Summarize the following meeting transcript:\n\n"
        f"{transcript}"
    )

    tasks_prompt = (
        "List the key action items from this meeting:\n\n"
        f"{transcript}"
    )

    summary = call_ollama(summary_prompt)
    action_items = call_ollama(tasks_prompt)

    return {
        "transcript": transcript.strip(),
        "summary": summary,
        "action_items": action_items
    }