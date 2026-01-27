from fastapi import FastAPI, UploadFile, File, Form
import base64
from backend.services import generate_caption

app = FastAPI(title="Image Caption Generator API", version="1.0")

@app.post("/caption/")
async def caption_image(
    file: UploadFile = File(...),
    tone: str = Form("Standard"),
    include_hashtags: bool = Form(False),
    custom_prompt: str = Form(None)
):
    """
    Endpoint to receive an image and generation parameters, and return a caption.
    """
    # Read and encode image
    image_bytes = await file.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    # Call service to generate caption
    caption = generate_caption(
        image_base64=image_base64,
        tone=tone,
        include_hashtags=include_hashtags,
        custom_prompt=custom_prompt
    )

    return {"caption": caption}
