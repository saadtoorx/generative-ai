"""
Code Review Assistant - Streamlit Frontend
Modern, engaging UI with multiple features.
"""
import streamlit as st
import requests
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Code Review Assistant",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding: 1rem 2rem;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    /* Stats cards */
    .stats-container {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        border-radius: 10px;
        flex: 1;
        text-align: center;
    }
    
    .stat-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #666;
    }
    
    /* Review type badges */
    .badge-general { background: #3498db; }
    .badge-bugs { background: #e74c3c; }
    .badge-quality { background: #2ecc71; }
    .badge-performance { background: #f39c12; }
    .badge-security { background: #9b59b6; }
    
    .review-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        color: white;
        font-weight: 600;
        font-size: 0.85rem;
        margin-bottom: 1rem;
    }
    
    /* History items */
    .history-item {
        padding: 0.75rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        cursor: pointer;
    }
    
    .history-item:hover {
        background: #e9ecef;
    }
    
    /* Status indicator */
    .status-connected { color: #2ecc71; }
    .status-disconnected { color: #e74c3c; }
    
    /* Toast notification */
    .toast {
        position: fixed;
        bottom: 20px;
        right: 20px;
        padding: 1rem 2rem;
        background: #2ecc71;
        color: white;
        border-radius: 8px;
        z-index: 1000;
        animation: fadeIn 0.3s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# Configuration
BACKEND_URL = "http://localhost:8000"

REVIEW_TYPES = {
    "🔍 General Review": "general",
    "🐛 Bug Detection": "bugs", 
    "✨ Code Quality": "quality",
    "⚡ Performance": "performance",
    "🔒 Security": "security"
}

SAMPLE_CODES = {
    "Python - Simple Function": '''def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    average = total / len(numbers)
    return average

result = calculate_average([1, 2, 3, 4, 5])
print(result)''',
    
    "Python - Security Issue": '''import sqlite3

def get_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchone()''',
    
    "JavaScript - Async Function": '''async function fetchUserData(userId) {
    const response = await fetch(`/api/users/${userId}`);
    const data = response.json();
    return data;
}

fetchUserData(123).then(user => {
    console.log(user.name);
});'''
}

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []
if "theme" not in st.session_state:
    st.session_state.theme = "light"


def check_backend_status():
    """Check if backend and Ollama are running."""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return True, data.get("ollama_status") == "connected", data.get("model", "unknown")
    except:
        pass
    return False, False, "unknown"


def get_code_review(code: str, review_type: str, language: str = None):
    """Get code review from backend."""
    try:
        response = requests.post(
            f"{BACKEND_URL}/review",
            json={
                "code": code,
                "review_type": review_type,
                "language": language
            },
            timeout=300
        )
        
        if response.status_code == 200:
            return response.json(), None
        else:
            error = response.json().get("detail", "Unknown error")
            return None, error
    except requests.exceptions.Timeout:
        return None, "Request timed out. Try with shorter code."
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to backend. Is it running?"
    except Exception as e:
        return None, str(e)


def add_to_history(code: str, review: str, review_type: str, stats: dict, response_time: float):
    """Add review to session history."""
    st.session_state.history.insert(0, {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "code_preview": code[:50] + "..." if len(code) > 50 else code,
        "review": review,
        "review_type": review_type,
        "stats": stats,
        "response_time": response_time
    })
    # Keep only last 10 reviews
    st.session_state.history = st.session_state.history[:10]


def export_as_markdown(review: str, code: str, review_type: str, stats: dict):
    """Generate markdown export."""
    return f"""# Code Review Report

**Review Type:** {review_type}  
**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Code Statistics
- Lines: {stats.get('lines', 'N/A')}
- Characters: {stats.get('characters', 'N/A')}
- Words: {stats.get('words', 'N/A')}

## Code
```
{code}
```

## Review
{review}

---
*Generated by Code Review Assistant*
"""


# ---- SIDEBAR ----
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    
    # Connection status
    backend_ok, ollama_ok, model = check_backend_status()
    
    st.markdown("### Connection Status")
    col1, col2 = st.columns(2)
    with col1:
        if backend_ok:
            st.markdown("🟢 Backend")
        else:
            st.markdown("🔴 Backend")
    with col2:
        if ollama_ok:
            st.markdown("🟢 Ollama")
        else:
            st.markdown("🔴 Ollama")
    
    if model != "unknown":
        st.caption(f"Model: {model}")
    
    st.divider()
    
    # Review type selection
    st.markdown("### Review Type")
    selected_type = st.selectbox(
        "Select review focus",
        options=list(REVIEW_TYPES.keys()),
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # Sample code loader
    st.markdown("### 📝 Sample Code")
    sample_choice = st.selectbox(
        "Load sample code",
        options=["None"] + list(SAMPLE_CODES.keys()),
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # History
    st.markdown("### 📜 Review History")
    if st.session_state.history:
        for i, item in enumerate(st.session_state.history[:5]):
            with st.expander(f"⏱️ {item['timestamp']} - {item['review_type']}"):
                st.caption(item['code_preview'])
                if st.button("Load this review", key=f"load_{i}"):
                    st.session_state.selected_history = item
    else:
        st.caption("No reviews yet")


# ---- MAIN CONTENT ----
# Header
st.markdown("""
<div class="header-container">
    <h1 class="header-title">🔍 Code Review Assistant</h1>
    <p class="header-subtitle">AI-powered code analysis with local LLM</p>
</div>
""", unsafe_allow_html=True)

# Main layout
col_main, col_result = st.columns([1, 1])

with col_main:
    st.markdown("### 📝 Your Code")
    
    # Pre-fill with sample if selected
    default_code = ""
    if sample_choice != "None":
        default_code = SAMPLE_CODES.get(sample_choice, "")
    
    code_input = st.text_area(
        "Paste your code here",
        value=default_code,
        height=400,
        label_visibility="collapsed",
        placeholder="Paste your code here for review..."
    )
    
    # Code stats preview
    if code_input:
        lines = code_input.count('\n') + 1
        chars = len(code_input)
        words = len(code_input.split())
        
        stat_cols = st.columns(3)
        with stat_cols[0]:
            st.metric("Lines", lines)
        with stat_cols[1]:
            st.metric("Characters", chars)
        with stat_cols[2]:
            st.metric("Words", words)
    
    # Action buttons
    btn_col1, btn_col2 = st.columns([2, 1])
    
    with btn_col1:
        review_button = st.button(
            "🚀 Get Review", 
            type="primary", 
            use_container_width=True,
            disabled=not (backend_ok and ollama_ok)
        )
    
    with btn_col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.rerun()


with col_result:
    st.markdown("### 📋 Review Results")
    
    if review_button:
        if not code_input.strip():
            st.error("⚠️ Please enter some code to review")
        else:
            review_type = REVIEW_TYPES[selected_type]
            
            with st.spinner(f"🔍 Analyzing code ({selected_type})..."):
                result, error = get_code_review(code_input, review_type)
            
            if error:
                st.error(f"❌ {error}")
            else:
                # Add to history
                add_to_history(
                    code_input,
                    result["review"],
                    result["review_type"],
                    result["stats"],
                    result["response_time"]
                )
                
                # Display review type badge
                badge_class = f"badge-{review_type}"
                st.markdown(f"""
                <span class="review-badge {badge_class}">
                    {selected_type}
                </span>
                """, unsafe_allow_html=True)
                
                # Response time
                st.caption(f"⏱️ Completed in {result['response_time']}s")
                
                # Review content
                st.markdown(result["review"])
                
                st.divider()
                
                # Action buttons
                action_cols = st.columns(2)
                
                with action_cols[0]:
                    # Copy button (using clipboard workaround)
                    if st.button("📋 Copy Review", use_container_width=True):
                        st.code(result["review"])
                        st.success("Review displayed above - select and copy!")
                
                with action_cols[1]:
                    # Export button
                    markdown_export = export_as_markdown(
                        result["review"],
                        code_input,
                        result["review_type"],
                        result["stats"]
                    )
                    st.download_button(
                        "📥 Export as Markdown",
                        data=markdown_export,
                        file_name=f"code_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
    
    # Show selected history item
    elif hasattr(st.session_state, 'selected_history') and st.session_state.selected_history:
        item = st.session_state.selected_history
        st.markdown(f"**Review Type:** {item['review_type']}")
        st.caption(f"⏱️ Response time: {item['response_time']}s")
        st.markdown(item['review'])
        
        if st.button("Clear selection"):
            st.session_state.selected_history = None
            st.rerun()
    else:
        # Empty state
        st.info("👈 Enter code and click **Get Review** to start")
        
        st.markdown("""
        **Tips:**
        - Select different review types for focused analysis
        - Use sample code to test the features
        - Export reviews as Markdown files
        - Review history is saved in the sidebar
        """)


# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #888; padding: 1rem;">
    <p>Powered by <strong>Ollama</strong> with <strong>CodeLlama</strong> | Built with <strong>FastAPI</strong> & <strong>Streamlit</strong></p>
</div>
""", unsafe_allow_html=True)