import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Medical Notes Structuring Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern Medical Theme
st.markdown("""
<style>
    /* Main Theme Colors */
    :root {
        --primary-color: #1e88e5;
        --secondary-color: #26a69a;
        --background-color: #f5f7fa;
        --card-background: #ffffff;
        --text-primary: #2c3e50;
        --text-secondary: #607d8b;
        --success-color: #4caf50;
        --warning-color: #ff9800;
        --error-color: #f44336;
    }
    
    /* Main Container */
    .main {
        background-color: var(--background-color);
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #1e88e5 0%, #1565c0 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(30, 136, 229, 0.3);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-size: 1.1rem;
    }
    
    /* Card Styling */
    .result-card {
        background: var(--card-background);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        border-left: 4px solid var(--primary-color);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .result-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.12);
    }
    
    /* Section Labels */
    .section-label {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .symptoms-label { background-color: #e3f2fd; color: #1565c0; }
    .diagnosis-label { background-color: #fce4ec; color: #c62828; }
    .medications-label { background-color: #e8f5e9; color: #2e7d32; }
    .followup-label { background-color: #fff3e0; color: #ef6c00; }
    
    /* Status Badges */
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .status-connected {
        background-color: #e8f5e9;
        color: #2e7d32;
    }
    
    .status-disconnected {
        background-color: #ffebee;
        color: #c62828;
    }
    
    /* Sidebar Styling */
    .sidebar-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #1e88e5 0%, #1565c0 100%);
        border-radius: 10px;
        color: white;
        margin-bottom: 1.5rem;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #1e88e5 0%, #1565c0 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(30, 136, 229, 0.4);
    }
    
    /* Input Styling */
    .stTextArea textarea {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 1rem;
    }
    
    .stTextArea textarea:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(30, 136, 229, 0.2);
    }
    
    /* Metrics */
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Backend Configuration
BACKEND_URL = "http://localhost:8000"


def check_backend_health():
    """Check if the backend API is running."""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None


def extract_note(note: str) -> dict:
    """Send a note to the backend for extraction."""
    try:
        response = requests.post(
            f"{BACKEND_URL}/extract/",
            data={"note": note},
            timeout=120
        )
        return response.json() if response.status_code == 200 else {"error": response.json().get("detail", "Unknown error")}
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to backend. Please ensure the server is running."}
    except Exception as e:
        return {"error": str(e)}


def parse_structured_data(structured_str: str) -> dict:
    """Parse the structured data from the API response."""
    try:
        # Try to parse as JSON
        data = json.loads(structured_str)
        return {
            "symptoms": data.get("symptoms", "Not specified"),
            "diagnosis": data.get("diagnosis", "Not specified"),
            "medications": data.get("medications", "Not specified"),
            "follow_up": data.get("follow_up", data.get("followUp", "Not specified"))
        }
    except json.JSONDecodeError:
        return {
            "symptoms": "N/A",
            "diagnosis": "N/A",
            "medications": "N/A",
            "follow_up": "N/A"
        }


def display_result_card(patient_id, data, index):
    """Display a single result in a styled card."""
    with st.expander(f"📋 Patient {patient_id}", expanded=(index == 0)):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<span class="section-label symptoms-label">🩺 Symptoms</span>', unsafe_allow_html=True)
            symptoms = data.get("symptoms", "Not specified")
            if isinstance(symptoms, list):
                symptoms = ", ".join(symptoms)
            st.write(symptoms)
            
            st.markdown('<span class="section-label diagnosis-label">📊 Diagnosis</span>', unsafe_allow_html=True)
            st.write(data.get("diagnosis", "Not specified"))
        
        with col2:
            st.markdown('<span class="section-label medications-label">💊 Medications</span>', unsafe_allow_html=True)
            medications = data.get("medications", "Not specified")
            if isinstance(medications, list):
                medications = ", ".join(medications)
            st.write(medications)
            
            st.markdown('<span class="section-label followup-label">📅 Follow-up</span>', unsafe_allow_html=True)
            st.write(data.get("follow_up", "Not specified"))


# Sample Data
SAMPLE_NOTES = [
    {
        "patient_id": "P001",
        "doctor_notes": "Patient presents with persistent headache, dizziness, and fatigue for the past 3 days. Blood pressure elevated at 150/95. Diagnosis: Hypertension Stage 1. Prescribed Lisinopril 10mg daily. Lifestyle modifications recommended. Follow-up in 2 weeks for BP monitoring."
    },
    {
        "patient_id": "P002",
        "doctor_notes": "Chief complaint: Severe sore throat, difficulty swallowing, and fever (101.5°F) for 2 days. Physical exam reveals swollen tonsils with white patches. Rapid strep test positive. Diagnosis: Streptococcal pharyngitis. Prescribed Amoxicillin 500mg TID for 10 days. Rest and increased fluid intake advised. Return if symptoms worsen."
    },
    {
        "patient_id": "P003",
        "doctor_notes": "Patient complains of joint pain in both knees, morning stiffness lasting over 30 minutes, and mild swelling. Symptoms ongoing for 6 months. X-ray shows joint space narrowing. Diagnosis: Osteoarthritis, bilateral knees. Prescribed Naproxen 500mg BID and physical therapy referral. Weight loss encouraged. Follow-up in 6 weeks."
    }
]


# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <h2>🏥 Medical Notes</h2>
        <p>Structuring Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📊 System Status")
    
    # Check backend health
    health = check_backend_health()
    
    if health:
        st.markdown("""
        <div class="status-badge status-connected">
            ✅ API Connected
        </div>
        """, unsafe_allow_html=True)
        st.caption(f"Ollama: {health.get('ollama_status', 'Unknown')}")
    else:
        st.markdown("""
        <div class="status-badge status-disconnected">
            ❌ API Disconnected
        </div>
        """, unsafe_allow_html=True)
        st.caption("Start the backend server to continue")
    
    st.markdown("---")
    
    st.markdown("### ℹ️ About")
    st.markdown("""
    This application uses **AI-powered extraction** to convert unstructured 
    doctor's notes into structured medical data.
    
    **Features:**
    - 📝 Single note analysis
    - 📁 Batch CSV processing
    - 📥 Export to CSV/JSON
    - 🔍 Intelligent extraction
    """)
    
    st.markdown("---")
    
    st.markdown("### 📖 Instructions")
    st.markdown("""
    1. Choose your input mode
    2. Enter or upload medical notes
    3. Click **Extract** to process
    4. Review and download results
    """)
    
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    show_raw_json = st.checkbox("Show raw JSON output", value=False)
    
    st.markdown("---")
    st.caption(f"Version 1.0.0 | {datetime.now().strftime('%Y-%m-%d')}")


# ========== MAIN CONTENT ==========

# Header
st.markdown("""
<div class="main-header">
    <h1>🏥 Medical Note Structuring Assistant</h1>
    <p>Transform unstructured clinical notes into organized medical data using AI</p>
</div>
""", unsafe_allow_html=True)

# Input Mode Selection
tab1, tab2 = st.tabs(["📝 Single Note", "📁 Batch Upload"])

# Initialize session state
if "results" not in st.session_state:
    st.session_state.results = []
if "processed" not in st.session_state:
    st.session_state.processed = False

# ========== SINGLE NOTE TAB ==========
with tab1:
    col_header, col_spacer, col_btn = st.columns([2, 1.5, 1])
    with col_header:
        st.markdown("### Enter Doctor's Note")
    with col_btn:
        st.write("") # Spacer for vertical alignment
        if st.button("📋 Load Sample", help="Load a sample doctor's note", use_container_width=True):
            st.session_state.sample_note = SAMPLE_NOTES[0]["doctor_notes"]
    
    # Text input
    default_note = st.session_state.get("sample_note", "")
    note_input = st.text_area(
        "Paste the doctor's note here:",
        value=default_note,
        height=200,
        placeholder="Enter the clinical note text here...\n\nExample: Patient presents with persistent cough and fever for 5 days. Chest X-ray shows infiltrates. Diagnosis: Community-acquired pneumonia. Prescribed Azithromycin 500mg..."
    )
    
    col1, col2, col3 = st.columns([1, 1, 3])
    
    with col1:
        extract_btn = st.button("🔍 Extract Information", type="primary", use_container_width=True)
    
    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.sample_note = ""
            st.session_state.single_result = None
            st.rerun()
    
    # Extract single note
    if extract_btn and note_input.strip():
        with st.spinner("🔄 Analyzing medical note..."):
            result = extract_note(note_input)
            
            if "error" in result:
                st.error(f"❌ {result['error']}")
            else:
                st.session_state.single_result = result
                st.success("✅ Extraction complete!")
    
    # Display single result
    if "single_result" in st.session_state and st.session_state.single_result:
        result = st.session_state.single_result
        structured = result.get("structured", "{}")
        parsed = parse_structured_data(structured)
        
        st.markdown("### 📊 Extracted Information")
        
        # Wrapped in a container for cleaner look
        with st.container():
            # Diagnosis (Full Width)
            st.markdown('<span class="section-label diagnosis-label">📊 Diagnosis</span>', unsafe_allow_html=True)
            st.info(parsed.get("diagnosis", "Not specified"))

            # Symptoms and Medications (2 Columns)
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<span class="section-label symptoms-label">🩺 Symptoms</span>', unsafe_allow_html=True)
                symptoms = parsed.get("symptoms", "Not specified")
                content = ""
                if isinstance(symptoms, list):
                    content = "\n".join([f"• {s}" for s in symptoms])
                else:
                    content = symptoms
                st.write(content)
            
            with col2:
                st.markdown('<span class="section-label medications-label">💊 Medications</span>', unsafe_allow_html=True)
                medications = parsed.get("medications", "Not specified")
                content = ""
                if isinstance(medications, list):
                    content = "\n".join([f"• {m}" for m in medications])
                else:
                    content = medications
                st.write(content)
                
            st.markdown("<br>", unsafe_allow_html=True)
                
            # Follow-up (Full Width)
            st.markdown('<span class="section-label followup-label">📅 Follow-up</span>', unsafe_allow_html=True)
            st.success(parsed.get("follow_up", "Not specified"))
        
        # Export options
        st.markdown("### 📥 Export")
        col1, col2, col3, col4 = st.columns([1, 1, 1, 2])
        
        with col1:
            st.download_button(
                "📄 JSON",
                json.dumps(parsed, indent=2),
                file_name="extracted_note.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col2:
            df = pd.DataFrame([parsed])
            st.download_button(
                "📊 CSV",
                df.to_csv(index=False),
                file_name="extracted_note.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col3:
            if st.button("📋 Copy", use_container_width=True):
                st.info("Use JSON download")
        
        # Raw JSON toggle
        if show_raw_json:
            with st.expander("🔧 Raw JSON Response"):
                st.code(structured, language="json")


# ========== BATCH UPLOAD TAB ==========
with tab2:
    col_header, col_spacer, col_btn = st.columns([2, 1.5, 1])
    with col_header:
        st.markdown("### Upload Clinical Notes CSV")
    with col_btn:
        st.write("") # Spacer
        if st.button("📥 Load Sample Data", help="Load sample CSV data", use_container_width=True):
            st.session_state.sample_df = pd.DataFrame(SAMPLE_NOTES)
    
    # Show expected format
    with st.expander("📋 Expected CSV Format"):
        st.markdown("""
        Your CSV file should have the following columns:
        - `patient_id`: Unique identifier for each patient
        - `doctor_notes`: The clinical note text
        
        **Example:**
        """)
        example_df = pd.DataFrame({
            "patient_id": ["001", "002"],
            "doctor_notes": [
                "Patient complains of fatigue and joint pain...",
                "Severe cough and shortness of breath..."
            ]
        })
        st.dataframe(example_df)
    
    # File upload or sample data
    uploaded_file = st.file_uploader(
        "Upload your CSV file",
        type=["csv"],
        help="Upload a CSV file with patient_id and doctor_notes columns"
    )
    
    # Use sample data if loaded
    if "sample_df" in st.session_state:
        st.info("📋 Using sample data. Upload a file to replace it.")
        st.dataframe(st.session_state.sample_df, use_container_width=True)
        df = st.session_state.sample_df
    elif uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ Loaded {len(df)} records")
        st.dataframe(df.head(), use_container_width=True)
    else:
        df = None
    
    # Process button
    if df is not None:
        col1, col2 = st.columns([1, 4])
        
        with col1:
            process_btn = st.button("🚀 Process Notes", type="primary", use_container_width=True)
        
        if process_btn:
            results = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, row in df.iterrows():
                progress = (idx + 1) / len(df)
                progress_bar.progress(progress)
                status_text.text(f"Processing note {idx + 1} of {len(df)}...")
                
                response = extract_note(row["doctor_notes"])
                
                if "error" in response:
                    st.warning(f"⚠️ Error processing patient {row['patient_id']}: {response['error']}")
                    parsed = {"symptoms": "Error", "diagnosis": "Error", "medications": "Error", "follow_up": "Error"}
                else:
                    structured = response.get("structured", "{}")
                    parsed = parse_structured_data(structured)
                
                results.append({
                    "patient_id": row["patient_id"],
                    **parsed
                })
            
            progress_bar.progress(1.0)
            status_text.text("✅ Processing complete!")
            
            st.session_state.batch_results = results
    
    # Display batch results
    if "batch_results" in st.session_state and st.session_state.batch_results:
        results = st.session_state.batch_results
        
        st.markdown("---")
        st.markdown("### 📊 Extraction Results")
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", len(results))
        with col2:
            success_count = sum(1 for r in results if r.get("diagnosis") != "Error")
            st.metric("Successful", success_count)
        with col3:
            st.metric("Failed", len(results) - success_count)
        
        # Display each result
        for idx, result in enumerate(results):
            display_result_card(result["patient_id"], result, idx)
        
        # Export options
        st.markdown("### 📥 Export Results")
        result_df = pd.DataFrame(results)
        
        col1, col2, col3 = st.columns([1, 1, 3])
        
        with col1:
            st.download_button(
                "📊 CSV",
                result_df.to_csv(index=False),
                file_name="structured_medical_notes.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            st.download_button(
                "📄 JSON",
                json.dumps(results, indent=2),
                file_name="structured_medical_notes.json",
                mime="application/json",
                use_container_width=True
            )
        
        # Results table
        with st.expander("📋 View Results Table"):
            st.dataframe(result_df, use_container_width=True)


# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #607d8b; padding: 1rem;">
    <p>Built by Saad Toor | saadtoorx</p>
</div>
""", unsafe_allow_html=True)
