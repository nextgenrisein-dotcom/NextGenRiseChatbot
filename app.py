import streamlit as st
from chatbot import ask
from PIL import Image
from pathlib import Path

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="NextGen Rise Academy AI",
    page_icon="",
    layout="wide"
)
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

html, body, [class*="css"], .stApp{
    font-family: 'Roboto', sans-serif;
}

h1,h2,h3,h4,h5,h6{
    font-family:'Roboto',sans-serif;
    font-weight:700;
}

.stButton>button{
    background:#0F766E;
    color:white;
    border-radius:12px;
    border:none;
    height:45px;
    font-family:'Roboto',sans-serif;
}

.stChatMessage{
    border-radius:18px;
    padding:14px;
}

.stChatInput{
    font-family:'Roboto',sans-serif;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

.main{
    background-color:#F8FAFC;
}

.stChatMessage{
    border-radius:15px;
    padding:12px;
}

h1{
    color:#0F4C81;
}

.footer{
    text-align:center;
    color:gray;
    font-size:13px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:
    # ==========================
# ADMIN PANEL
# ==========================

    st.sidebar.markdown("---")
    st.sidebar.header("Admin Panel")

admin_password = st.sidebar.text_input(
    "Enter Admin Password",
    type="password"
)

# Change this password
ADMIN_PASSWORD = "NextGen@2026"


if admin_password == ADMIN_PASSWORD:

    st.sidebar.success("Admin access granted")

    uploaded_file = st.sidebar.file_uploader(
        "Upload New PDF",
        type=["pdf"]
    )

    if uploaded_file:

        import os

        os.makedirs("data", exist_ok=True)

        file_path = os.path.join(
            "data",
            uploaded_file.name
        )

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())


        st.sidebar.success(
            f"Saved: {uploaded_file.name}"
        )


        st.sidebar.info(
            "PDF uploaded successfully. "
            "Rebuild the knowledge base to make the chatbot learn it."
        )


elif admin_password:

    st.sidebar.error(
        "Incorrect password"
    )

    logo = Path("images/logo.png")

    if logo.exists():
        st.image(str(logo), width=170)

    st.title("NextGen Rise Academy")

    st.markdown("---")

    st.write("### About")
    from pathlib import Path

pdfs = list(Path("data").glob("*.pdf"))

st.sidebar.markdown("---")
st.sidebar.metric(
    "Knowledge Base",
    f"{len(pdfs)} PDFs"
)

st.markdown(
    """
    <div style="
        font-family: 'Times New Roman', serif;
        font-size: 18px;
        line-height: 1.3;
    ">

    <b style="color:#0B3D91; font-size:22px;">
    Welcome to the NextGen Rise Academy AI Assistant
    </b>

    <p>
    Your intelligent learning companion designed to provide information about:
    </p>

    <b style="color:#008000;">• Courses</b> - Available training programs and learning pathways.<br>

    <b style="color:#D2691E;">• Admissions</b> - Enrollment process and requirements.<br>

    <b style="color:#8B008B;">• Fees</b> - Course costs and payment details.<br>

    <b style="color:#006400;">• Training</b> - Skills development programs and opportunities.<br>

    <b style="color:#B22222;">• Certifications</b> - Professional certification pathways.<br>

    <b style="color:#1E90FF;">• NextGen Rise Initiative</b> - Building skills, creating opportunities, and inspiring growth.

    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("---")

if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# -----------------------------
# Main Page
# -----------------------------

st.title("NextGen Rise Academy AI Assistant")
st.info(
    """
**Welcome to NextGen Rise Academy AI**

I can help you with:

- Course information
- Admissions
- Fees
- Training schedules
- Certifications
- Frequently asked questions
- NextGen Rise Initiative

Ask me anything!
"""
)

st.caption(
    "Powered by Groq • Llama 3.3 • LangChain • FAISS"
)

# -----------------------------
# Chat History
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# -----------------------------
# User Input
# -----------------------------
st.subheader("Quick Questions")

col1, col2 = st.columns(2)

with col1:
    if st.button("What courses do you offer?"):
        st.session_state.quick_question = "What courses do you offer?"

with col2:
    if st.button("How do I enroll?"):
        st.session_state.quick_question = "How do I enroll?"

if "quick_question" in st.session_state:
    prompt = st.session_state.quick_question
    del st.session_state.quick_question
else:
    prompt = st.chat_input("Ask anything...")
prompt = st.chat_input(
    "Ask a question about NextGen Rise Academy..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Searching NextGen Rise knowledge base..."):

            try:

                answer = ask(prompt)

            except Exception as e:

                answer = f"Error: {e}"

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":answer
        }
    )

st.markdown("---")

st.markdown("""
---
<div style="text-align:center; font-family:Roboto;">

<h4>NextGen Rise Academy AI</h4>

<p>
Powered by <b>NextGen Rise Initiative</b><br>
Building Skills • Creating Opportunities • Inspiring Growth<br><br>
© 2026 NextGen Rise Initiative
</p>

</div>
""", unsafe_allow_html=True)