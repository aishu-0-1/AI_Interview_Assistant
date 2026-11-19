import streamlit as st
from groq import Groq
st.set_page_config( page_title="AI_Interview_Assistant",page_icon="🎃", layout="centered")
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
    [ "Machine Learning Engineer", "Senior Software Engineer","DevOps Engineer","Data Analyst","Prompt Engineer", "Other"])
if role == "Other":
    custom_role = st.text_input("Enter your Job Title")
    if custom_role.strip():
        role = custom_role
gen_model = st.selectbox("Model",["openai/gpt-oss-20b", "openai/gpt-oss-120b"])
level = st.selectbox( "Difficulty", ["Beginner", "Intermediate", "Advanced"])
mode = st.radio( "Activity", ["Generate Questions","Generate Code Questions", "Evaluate Answers","Improve Answers" ])
if mode == "Generate Questions":
    count = st.slider("Number of Questions", 1, 10, 5)
elif mode == "Generate Code Questions":
    topic = st.selectbox("Topics", ["SQL", "DBMS", "C/C++", "AI/ML", "Java", "CSS", "Python"]  )
    count = st.slider("Number of Questions", 1, 10, 5)
else:
    question = st.text_area("Enter Interview Question")
    answer = st.text_area("Enter Your Answer", height=160)
if st.button("Generate AI Response", type="primary"):
    if mode in ["Evaluate Answers", "Improve Answers"]:
        if not question.strip() or not answer.strip():
            st.warning("Please enter both Question and Answer.")
            st.stop()
    if mode == "Generate Questions":
        task = ( task = "Generate" + str(count) + "Frequently asked Interview Questions, 3 theory and 2 scenario questions.Do not give answers. Give the hint")
    elif mode == "Generate Code Questions":
        task = ( "Generate" + str(count) + "Frequently asked coding questions on topic" + topic +"and give hints to solve them. Be accurate." )
    elif mode == "Evaluate Answers":
        task = ("Question :" + question +"My answer : " + answer + " Evaluate this answers based on concept, relevance, communication, length of answer .G ive each rating out of  5 in the list.")
    elif mode == "Improve Answers":
        task = ("Question :" + question +"My answer : " + answer + " Improve my answer and give the correct answer in simple English.")
    background ="Job role :" + role + " Difficulti level " + level 
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
