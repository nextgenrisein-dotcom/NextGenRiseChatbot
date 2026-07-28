import streamlit as st
from chatbot import ask, speech_to_text
from pathlib import Path
from PIL import Image
import os


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------


# Load chatbot icon
chatbot_icon = Image.open(
    "images/logo.png"
)


st.set_page_config(
    page_title="NextGen Rise Academy AI",
    page_icon=chatbot_icon,
    layout="wide"
)



# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
"""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap'
);


html, body, [class*="css"], .stApp {

    font-family:'Roboto', sans-serif;
    background:#F8FAFC;

}


h1,h2,h3,h4,h5,h6{

    font-weight:700;

}


.stButton>button{

    background:#0F766E;
    color:white;
    border-radius:12px;
    border:none;
    height:45px;

}


.stChatMessage{

    border-radius:18px;
    padding:14px;

}


.footer{

    text-align:center;
    color:gray;
    font-size:13px;

}

</style>

""",
unsafe_allow_html=True
)




# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:


    logo = Path("images/logo.png")


    if logo.exists():

        st.image(
            str(logo),
            width=170
        )



    st.markdown("---")



    st.markdown(
    """

    <h3 style="font-weight:700;color:black;">

    Welcome to the NextGen Rise Academy AI Assistant

    </h3>


    <p style="color:black;">

    Your intelligent learning companion designed to provide information about:

    <br><br>

    <b>• Courses</b> - Available training programs and learning pathways.

    <br><br>

    <b>• Admissions</b> - Enrollment process and requirements.

    <br><br>

    <b>• Fees</b> - Course costs and payment details.

    <br><br>

    <b>• Training</b> - Skills development programs and opportunities.

    <br><br>

    <b>• Certifications</b> - Professional certification pathways.

    </p>

    """,

    unsafe_allow_html=True

    )



    # -----------------------------
    # ADMIN PANEL
    # -----------------------------

    st.markdown("---")


    st.header(
        "Admin Panel"
    )


    admin_password = st.text_input(
        "Enter Admin Password",
        type="password"
    )


    ADMIN_PASSWORD = "NextGen@2026"



    if admin_password == ADMIN_PASSWORD:


        st.success(
            "Admin access granted"
        )


        uploaded_file = st.file_uploader(
            "Upload New PDF",
            type=["pdf"]
        )


        if uploaded_file:


            os.makedirs(
                "data",
                exist_ok=True
            )


            file_path = os.path.join(
                "data",
                uploaded_file.name
            )


            with open(
                file_path,
                "wb"
            ) as f:

                f.write(
                    uploaded_file.getbuffer()
                )


            st.success(
                f"Saved: {uploaded_file.name}"
            )


            st.info(
            """
            PDF uploaded successfully.
            Rebuild the knowledge base
            to make the chatbot learn it.
            """
            )


    elif admin_password:


        st.error(
            "Incorrect password"
        )



    pdfs = list(
        Path("data").glob("*.pdf")
    )


    st.markdown("---")


    st.metric(
        "Knowledge Base",
        f"{len(pdfs)} PDFs"
    )





# --------------------------------------------------
# MAIN PAGE
# --------------------------------------------------

st.title(
    "NextGen Rise Academy AI Assistant"
)



st.info(
"""
**Welcome to NextGen Rise Academy AI**

I can help you with course information, admissions, fees,
training schedules, certifications, frequently asked questions,
and information about the NextGen Rise Initiative.
Ask me anything!
"""
)



st.caption(
"Powered by Groq • Llama 3.3 • LangChain • FAISS"
)




# --------------------------------------------------
# CHAT HISTORY
# --------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []



for message in st.session_state.messages:


    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )





# --------------------------------------------------
# QUESTION AREA
# --------------------------------------------------

st.markdown("---")



st.markdown(
"""
<h3 style="
text-align:center;
color:#0F4C81;
">

Ask a question about NextGen Rise Academy

</h3>

""",
unsafe_allow_html=True
)



col1, col2 = st.columns(2)



# --------------------------------------------------
# VOICE INPUT
# --------------------------------------------------

with col1:


    voice_file = st.file_uploader(

        "Ask using Voice",

        type=[

            "mp3",
            "wav",
            "m4a",
            "webm"

        ]

    )



    if voice_file:


        st.audio(
            voice_file
        )


        if st.button(
            "Convert Voice to Text"
        ):


            with st.spinner(
                "Converting voice..."
            ):


                try:


                    voice_text = speech_to_text(
                        voice_file
                    )


                    st.session_state.voice_prompt = voice_text



                    st.success(
                        "Voice converted successfully"
                    )


                    st.write(
                        "Recognized question:"
                    )


                    st.write(
                        voice_text
                    )


                except Exception as e:


                    st.error(
                        f"Voice error: {e}"
                    )





# --------------------------------------------------
# IMAGE UPLOAD
# --------------------------------------------------

with col2:


    image_file = st.file_uploader(

        "Upload Image",

        type=[

            "png",
            "jpg",
            "jpeg"

        ]

    )


    if image_file:


        st.image(
            image_file,
            width=250
        )





# --------------------------------------------------
# INPUT HANDLING
# --------------------------------------------------

if "voice_prompt" in st.session_state:


    prompt = st.session_state.voice_prompt


    del st.session_state.voice_prompt



else:


    prompt = st.chat_input(
        "Ask a question about NextGen Rise Academy..."
    )





# --------------------------------------------------
# AI RESPONSE
# --------------------------------------------------

if prompt:


    st.session_state.messages.append(
    {
        "role":"user",
        "content":prompt
    }
    )



    with st.chat_message(
        "user"
    ):


        st.markdown(
            prompt
        )



    with st.chat_message(
        "assistant"
    ):


        with st.spinner(
            "Searching NextGen Rise knowledge base..."
        ):


            try:

                answer = ask(
                    prompt
                )


            except Exception as e:

                answer = f"Error: {e}"



        st.markdown(
            answer
        )



    st.session_state.messages.append(
    {
        "role":"assistant",
        "content":answer
    }
    )





# --------------------------------------------------
# CLEAR CHAT
# --------------------------------------------------

st.markdown("---")



if st.button(
    "Clear Chat"
):

    st.session_state.messages = []

    st.rerun()





# --------------------------------------------------
# LOWER INFORMATION SECTION
# --------------------------------------------------

st.markdown("---")



with st.expander(
    "About NextGen Rise Academy"
):

    st.write(
"""
NextGen Rise Academy, powered by NextGen Rise Initiative,
is a digital learning platform focused on empowering learners
with practical skills, professional training, and career opportunities.
"""
)



with st.expander(
    "Learning Areas"
):

    st.write(
"""
• Data Analysis

• Business Intelligence

• Programming

• Digital Skills

• Graphics Design

• Professional Certification Programs
"""
)





# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")



st.markdown(
"""
<div class="footer">

<h4>
NextGen Rise Academy AI
</h4>


Powered by <b>NextGen Rise Initiative</b><br>


Building Skills • Creating Opportunities • Inspiring Growth


<br><br>


© 2026 NextGen Rise Initiative


</div>

""",

unsafe_allow_html=True
)