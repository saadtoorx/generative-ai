import streamlit as st
import requests
import json
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Meeting Notes Generator",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
API_URL = "http://localhost:8000"

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
        color: #1e1e1e;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #ff3333;
        border-color: #ff3333;
    }
    .reportview-container .main .block-container {
        padding-top: 2rem;
    }
    h1 {
        color: #ff4b4b;
    }
    h2, h3 {
        color: #333;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .summary-box {
        background-color: #e8f4f9;
        color: #000000;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 5px solid #00a8e8;
        margin-bottom: 1rem;
    }
    .action-box {
        background-color: #f0fdf4;
        color: #000000;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 5px solid #4ade80;
        margin-bottom: 1rem;
    }
    .topic-tag {
        display: inline-block;
        background-color: #f1f5f9;
        color: #475569;
        padding: 0.2rem 0.8rem;
        border-radius: 1rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
        border: 1px solid #cbd5e1;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []

if 'current_result' not in st.session_state:
    st.session_state.current_result = None

def save_to_history(filename, result):
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "filename": filename,
        "result": result
    }
    st.session_state.history.insert(0, entry)

def load_from_history(index):
    st.session_state.current_result = st.session_state.history[index]["result"]

# Sidebar
with st.sidebar:
    st.title("🎙️ AI Notes Gen")
    st.markdown("---")
    
    st.subheader("About")
    st.info(
        "Upload a meeting recording to automatically generate transcripts, contributions, summarizations, and action items."
    )
    
    st.subheader("⚙️ Settings")

    
    st.markdown("---")
    st.subheader("🕑 Session History")
    
    if not st.session_state.history:
        st.text("No history yet.")
    else:
        for i, item in enumerate(st.session_state.history):
            if st.button(f"{item['timestamp']} - {item['filename']}", key=f"hist_{i}"):
                load_from_history(i)
                st.rerun()

    st.markdown("---")
    st.markdown("Made with ❤️ for School of AI")

# Main Content
col1, col2 = st.columns([3, 1])

with col1:
    st.title("Meeting Notes Generator")
    st.markdown("#### Transform your meeting audio into structured notes in seconds.")

with col2:
    # Health check status indicator
    with st.spinner("Checking backend status..."):
        try:
            # Increased timeout and added error logging
            health = requests.get(f"{API_URL}/health", timeout=5)
            if health.status_code == 200:
                st.success(f"Backend: Online 🟢")
            else:
                st.error(f"Backend: Error {health.status_code} 🔴")
        except requests.exceptions.ConnectionError:
            st.error("Backend: Offline (Connection Refused) 🔴 - Ensure 'main.py' is running.")
        except Exception as e:
            st.error(f"Backend: Error ({str(e)}) 🔴")

# File Upload Section
st.markdown("---")
uploaded_file = st.file_uploader("Upload Meeting Recording", type=['mp3', 'wav', 'm4a', 'flac', 'ogg'], help="Supported formats: MP3, WAV, M4A, FLAC, OGG")

if not uploaded_file and not st.session_state.current_result:
    st.info("👆 Start by uploading an audio file above.")

audio_file = uploaded_file # Alias for compatibility

if audio_file:
    # Display audio player and metadata
    col_audio, col_meta = st.columns([2, 1])
    with col_audio:
        st.audio(audio_file)
    with col_meta:
        st.caption(f"Filename: {audio_file.name}")
        st.caption(f"Size: {audio_file.size / (1024*1024):.2f} MB")
        st.caption(f"Type: {audio_file.type}")

    # Generate Button
    if st.button("🚀 Generate Meeting Notes", use_container_width=True):
        if not audio_file:
            st.warning("Please upload a file first.")
        else:
            try:
                # Progress bar and status
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("Uploading file...")
                progress_bar.progress(10)
                
                # API Call
                files = {"file": (audio_file.name, audio_file, audio_file.type)}
                
                status_text.text("Transcribing audio (this may take a while)...")
                progress_bar.progress(30)
                
                start_time = time.time()
                response = requests.post(f"{API_URL}/process/", files=files, timeout=600)
                
                if response.status_code == 200:
                    status_text.text("Analyzing content and generating summary...")
                    progress_bar.progress(80)
                    
                    result = response.json()
                    st.session_state.current_result = result
                    save_to_history(audio_file.name, result)
                    
                    progress_bar.progress(100)
                    status_text.text("Processing complete!")
                    time.sleep(1)
                    status_text.empty()
                    progress_bar.empty()
                    
                    st.toast("Meeting notes generated successfully!", icon="✅")
                    st.rerun()
                    
                else:
                    status_text.empty()
                    progress_bar.empty()
                    st.error(f"Error: {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to backend. Is the server running?")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Display Results
if st.session_state.current_result:
    result = st.session_state.current_result
    
    st.markdown("---")
    st.subheader("📊 Meeting Overview")
    
    # Metrics
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Processing Time", f"{result['processing_time']}s")
    with m2:
        st.metric("Word Count", result['word_count'])
    with m3:
        words_per_min = int(result['word_count'] / (result['processing_time'] / 60)) if result['processing_time'] > 0 else 0
        st.metric("Speed (wpm)", words_per_min)
        
    # Key Topics
    st.markdown("#### 🏷️ Key Topics")
    topics_html = ""
    for topic in result.get('key_topics', '').split(','):
        if topic.strip():
            topics_html += f'<span class="topic-tag">{topic.strip()}</span>'
    st.markdown(topics_html, unsafe_allow_html=True)
    
    # Summary
    st.markdown("### 📝 Executive Summary")
    st.markdown(f'<div class="summary-box">{result["summary"]}</div>', unsafe_allow_html=True)
    
    # Action Items
    st.markdown("### ✅ Action Items")
    st.markdown(f'<div class="action-box">{result["action_items"]}</div>', unsafe_allow_html=True)
    
    # Full Transcript
    with st.expander("📄 View Full Transcript", expanded=False):
        st.text_area("Transcript", value=result["transcript"], height=400)
        st.info("💡 You can copy the transcript from the box above.")
        
    # Export Options
    st.markdown("### 💾 Export")
    col_dl1, col_dl2 = st.columns(2)
    
    # Text Download
    text_content = f"""MEETING NOTES
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M")}

SUMMARY:
{result['summary']}

ACTION ITEMS:
{result['action_items']}

KEY TOPICS:
{result['key_topics']}

TRANSCRIPT:
{result['transcript']}
"""
    with col_dl1:
        st.download_button(
            label="📄 Download as Text",
            data=text_content,
            file_name=f"meeting_notes_{int(time.time())}.txt",
            mime="text/plain",
            use_container_width=True
        )
        
    # Markdown Download
    md_content = f"""# Meeting Notes
**Generated on:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

## 📝 Executive Summary
{result['summary']}

## ✅ Action Items
{result['action_items']}

## 🏷️ Key Topics
{result['key_topics']}

## 📄 Transcript
{result['transcript']}
"""
    with col_dl2:
        st.download_button(
            label="markdown Download as Markdown",
            data=md_content,
            file_name=f"meeting_notes_{int(time.time())}.md",
            mime="text/markdown",
            use_container_width=True
        )

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "AI Meeting Notes Generator | Powered by Whisper & Ollama"
    "</div>",
    unsafe_allow_html=True
)
