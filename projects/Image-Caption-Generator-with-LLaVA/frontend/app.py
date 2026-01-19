import streamlit as st
import requests
from gtts import gTTS
import io

# Page Config
st.set_page_config(
    page_title="Pro Image Caption AI",
    page_icon="📸",
    layout="wide"
)

# Sidebar
st.sidebar.title("Configuration")
st.sidebar.info("Ensure Ollama is running locally with 'llava' model.")
api_url = st.sidebar.text_input("API URL", "http://localhost:8000/caption/")

st.sidebar.markdown("---")
st.sidebar.header("About")
st.sidebar.markdown("""
This app generic smart captions for your images using the **LLaVA** model running locally via **Ollama**.
                    
**Features:**
- 🎭 Multiple Tones
- #️⃣ Hashtag Generator
- 🗣️ Text-to-Speech
- 📜 History
""")

# Main Content
st.title("📸 Pro Image Caption Generator")
st.markdown("Turns your images into engaging text!")

col1, col2 = st.columns([1, 1])

# Session State for History
if "history" not in st.session_state:
    st.session_state.history = []

with col1:
    st.subheader("1. Upload Image")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    st.subheader("2. Customize")
    tone = st.selectbox("Select Tone", ["Standard", "Professional", "Funny", "Creative", "Social Media"])
    include_hashtags = st.checkbox("Generate Hashtags")
    
    with st.expander("Advanced: Custom Prompt"):
        custom_prompt = st.text_input("Override prompt (optional)", help="Leave empty to use automatic prompts based on tone.")

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Preview", use_container_width=True)

        if st.button("✨ Generate Caption", type="primary"):
            with st.spinner("Analyzing image... (this may take a moment)"):
                try:
                    files = {"file": uploaded_file.getvalue()}
                    data = {
                        "tone": tone,
                        "include_hashtags": include_hashtags,
                        "custom_prompt": custom_prompt if custom_prompt else None
                    }
                    
                    response = requests.post(api_url, files=files, data=data)
                    response.raise_for_status()
                    
                    caption = response.json().get("caption", "Error: No caption returned.")
                    
                    # Save to history
                    st.session_state.history.insert(0, {"image": uploaded_file, "caption": caption})
                    
                    # Force refresh to show in result column immediately if wanted, 
                    # but simple variable passing is better for this flow.
                    st.session_state.latest_caption = caption

                except Exception as e:
                    st.error(f"Error: {e}")

with col2:
    st.subheader("3. Result")
    if "latest_caption" in st.session_state:
        caption_text = st.session_state.latest_caption
        
        st.success("Caption Generated Successfully!")
        st.markdown(f"""
        <div style="padding: 20px; border-radius: 10px; background-color: #f0f2f6; color: #333;">
            <p style="font-size: 18px; font-weight: 500;">{caption_text}</p>
        </div>
        """, unsafe_allow_html=True)

        # Audio (TTS)
        tts = gTTS(text=caption_text, lang='en')
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        st.audio(audio_buffer, format='audio/mp3')

        st.download_button(
            label="📥 Download Text",
            data=caption_text,
            file_name="caption.txt",
            mime="text/plain"
        )
    else:
        st.info("Upload an image and click Generate to see results here.")

# History Section
st.markdown("---")
st.subheader("📜 Recent History")
if st.session_state.history:
    for idx, item in enumerate(st.session_state.history):
        with st.expander(f"Caption {idx+1}"):
            h_col1, h_col2 = st.columns([1, 4])
            with h_col1:
                st.image(item["image"], width=100)
            with h_col2:
                st.write(item["caption"])
else:
    st.text("No history yet.")