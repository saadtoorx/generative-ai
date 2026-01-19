import requests
import logging
from backend.config import OLLAMA_API_URL, MODEL_NAME

# Setup simple logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_caption(image_base64: str, tone: str = "Standard", include_hashtags: bool = False, custom_prompt: str = None) -> str:
    """
    Sends a request to the Ollama API to generate a caption for the given image.
    
    Args:
        image_base64: The base64 encoded image string.
        tone: The desired tone of the caption (e.g., Funny, Professional).
        include_hashtags: Whether to generate hashtags.
        custom_prompt: Optional user-provided custom instruction.
        
    Returns:
        The generated caption text.
    """
    
    # Base prompt construction
    if custom_prompt:
        prompt = custom_prompt
    else:
        # Tone-based prompt modification
        prompt_templates = {
            "Standard": "Describe this image in one detailed sentence.",
            "Professional": "Provide a professional, objective description of the image content suitable for a business context.",
            "Funny": "Write a humorous and witty caption for this image.",
            "Creative": "Write a creative, poetic, or storytelling caption for this image.",
            "Social Media": "Write an engaging social media caption for this image that would get many likes.",
        }
        prompt = prompt_templates.get(tone, prompt_templates["Standard"])

    # Hashtag instruction
    if include_hashtags:
        prompt += " Also generate 5 to 10 relevant and trending hashtags at the end of the caption."

    logger.info(f"Sending request to Ollama with model={MODEL_NAME}, tone={tone}")

    try:
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "images": [image_base64],
                "stream": False
            },
            timeout=300  # increased timeout for slower models
        )
        response.raise_for_status()
        result = response.json()
        caption = result.get("response", "").strip()
        return caption

    except requests.exceptions.RequestException as e:
        logger.error(f"Error communicating with Ollama: {e}")
        return f"Error: Failed to generate caption. Is Ollama running? Details: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return "Error: An unexpected error occurred."
