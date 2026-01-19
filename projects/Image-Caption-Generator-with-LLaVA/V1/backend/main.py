from fastapi import FastAPI, UploadFile, File
import requests
import base64

app = FastAPI()

@app.post("/caption/")
async def caption_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llava",
            "prompt": "Describe this image in one sentence.",
            "images": [image_base64],
            "stream": False
        }
    )

    result = response.json()
    return {"caption": result["response"].strip()}