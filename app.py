
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="AI_Interview_Assistant",
    page_icon="🎃",
    layout="centered"
)

st.title("🎯 AI_Interview_Assistant")
st.caption("Practice and prepare for your placement here")
st.caption("Launched By Aishwarya S M")

# API connection
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("API Key is missing. Add it in Streamlit Cloud Secrets.")
    st.stop()

# Job role
role = st.selectbox(
    "Job Title",
    [
        "Machine Learning Engineer",
        "Senior Software Engineer",
        "DevOps Engineer",
        "Data Analyst",
        "Prompt Engineer",
        "Other"
    ]
)

if role == "Other":
    custom_role = st.text_input("Enter your Job Title")
    if custom_role.strip():
        role = custom_role

# Model selection
gen_model = st.selectbox(
    "Model",
    ["openai/gpt-oss-20b", "openai/gpt-oss-120b"]
)

# Difficulty level
level = st.selectbox(
    "Difficulty",
    ["Beginner", "Intermediate", "Advanced"]
)

# Activity
mode = st.radio(
    "Activity",
    [
        "Generate Questions",
        "Generate Code Questions",
        "Evaluate Answers",
        "Improve Answers"
    ]
)

# Input section
if mode == "Generate Questions":
    count = st.slider("Number of Questions", 1, 10, 5)

elif mode == "Generate Code Questions":
    topic = st.selectbox(
        "Topics",
        ["SQL", "DBMS", "C/C++", "AI/ML", "Java", "CSS", "Python"]
    )
    count = st.slider("Number of Questions", 1, 10, 5)

else:
    question = st.text_area("Enter Interview Question")
    answer = st.text_area("Enter Your Answer", height=160)

# Generate button
if st.button("Generate AI Response", type="primary"):

    # Validation
    if mode in ["Evaluate Answers", "Improve Answers"]:
        if not question.strip() or not answer.strip():
            st.warning("Please enter both Question and Answer.")
            st.stop()

    # Prompt creation
    if mode == "Generate Questions":
        task = (
            f"Generate {count} frequently asked interview questions "
            f"for the job role {role}. Include theory and scenario-based "
            f"questions. Do not provide answers. Give hints."
        )

    elif mode == "Generate Code Questions":
        task = (
            f"Generate {count} frequently asked coding interview questions "
            f"on {topic} for the job role {role}. "
            f"Give hints to solve them. Be accurate."
        )

    elif mode == "Evaluate Answers":
        task = (
            f"Question: {question}\n"
            f"My Answer: {answer}\n"
            "Evaluate my answer based on concept, relevance, communication, "
            "and completeness. Give ratings out of 5 and feedback."
        )

    elif mode == "Improve Answers":
        task = (
            f"Question: {question}\n"
            f"My Answer: {answer}\n"
            "Improve my answer and give the correct answer in simple English."
        )

    # Background information
    background = f"Job Role: {role}\nDifficulty Level: {level}\n"

    # AI response
    with st.spinner("Generating your answer..."):
        try:
            response = client.chat.completions.create(
                model=gen_model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Act as a senior interviewer with HR and "
                            "technical expertise. Give accurate and clear answers."
                        )
                    },
                    {
                        "role": "user",
                        "content": background + task
                    }
                ],
                temperature=0.7,
                max_tokens=1800
            )

            output = response.choices[0].message.content

            st.subheader("AI Response")
            st.markdown(output)

            st.download_button(
                "Download Response",
                output,
                file_name="Interview_Response.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"API connection failed: {e}")

st.caption("Powered by Streamlit.io and Github. Using LLM API")
