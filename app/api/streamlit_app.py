import requests
import streamlit as st

# -----------------------------------------------------
# Configuration
# -----------------------------------------------------

API_URL = "http://127.0.0.1:8000/chat"

st.set_page_config(
    page_title="SHL Assessment Recommendation System",
    layout="wide",
)

# -----------------------------------------------------
# Minimal CSS
# -----------------------------------------------------

st.markdown("""
<style>

.block-container{
    max-width:1100px;
    padding-top:2rem;
    padding-bottom:2rem;
}

hr{
    margin-top:0.7rem;
    margin-bottom:0.7rem;
}

.recommendation{
    padding-top:0.5rem;
    padding-bottom:0.8rem;
}

.small{
    color:gray;
    font-size:14px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------
# Session State
# -----------------------------------------------------

if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "latest_recommendations" not in st.session_state:
    st.session_state.latest_recommendations = []

# -----------------------------------------------------
# Header
# -----------------------------------------------------

title_col, button_col = st.columns([8,1])

with title_col:

    st.title("SHL Assessment Recommendation System")

    st.caption(
        "Hybrid Retrieval • BM25 • FAISS • Conversation Memory"
    )

with button_col:

    st.write("")

    if st.button("New Chat"):

        st.session_state.conversation = []
        st.session_state.latest_recommendations = []
        st.rerun()

st.divider()

# -----------------------------------------------------
# Empty Page
# -----------------------------------------------------

if len(st.session_state.conversation) == 0:

    st.markdown("### Start a conversation")

    st.markdown(
"""
Example queries

- Graduate Java Engineer
- Graduate Python Developer
- Sales Manager under 20 minutes
- Compare OPQ and Verify G
- Also include personality
- Remove Narrative Report
"""
    )

# -----------------------------------------------------
# Show Conversation
# -----------------------------------------------------

for message in st.session_state.conversation:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# -----------------------------------------------------
# Chat Input
# -----------------------------------------------------

prompt = st.chat_input("Ask about SHL assessments")

if prompt:

    st.session_state.conversation.append(
        {
            "role":"user",
            "content":prompt
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    payload = {
        "conversation": st.session_state.conversation
    }

    with st.spinner("Searching assessment catalog..."):

        try:

            response = requests.post(API_URL, json=payload)

            if response.status_code != 200:

                assistant_reply = f"Backend returned {response.status_code}"

                recommendations = []

            else:

                data = response.json()

                assistant_reply = data["reply"]

                recommendations = data.get(
                    "recommendations",
                    []
                )

        except Exception as e:

            assistant_reply = str(e)

            recommendations = []

    st.session_state.conversation.append(
        {
            "role":"assistant",
            "content":assistant_reply
        }
    )

    st.session_state.latest_recommendations = recommendations

    with st.chat_message("assistant"):

        st.markdown(assistant_reply)

        if recommendations:

            st.divider()

            st.subheader("Recommended Assessments")

            for i, rec in enumerate(recommendations, start=1):

                st.markdown(
f"""
### {i}. {rec['name']}

**Assessment Type**

{rec['assessment_type']}

**Job Level**

{rec['job_level']}

**Duration**

{rec['duration']}

**SHL Assessment**

{rec['url']}
"""
                )

                if i != len(recommendations):
                    st.divider()

# -----------------------------------------------------
# Footer
# -----------------------------------------------------

st.divider()

st.caption(
    "Built using FastAPI, Streamlit, BM25, FAISS, Sentence Transformers and GPT."
)