import streamlit as st
from groq import Groq
st.set_page_config(page_title = "AI_Assistant", page_icon ="🤩", layout = "centered")
st.title("AI_Interview_Assitant")
st.caption("Practice and prepare your placements here")
st.caption("Launched by LOHITA R PATIL")
try:
  client = Groq(api_key = st.secrets["GROQ_API_KEY"])
except (KeyError, FileNotFoundError):
  st.error("API key is missing Add it in advance setting")
  st.stop()
role = st.selectbox("Job Title", ["ML engineer", "DevOps engineer", "Software developer", "Software Engineer", "Prompt engineer", "Data analyst", "Other"])
if role == "Other":
  st.text_input("Enter the job title","XXXXXXXX")
gen_model = st.selectbox("Model",["openai/gpt-oss-20b", "openai/gpt-oss-120b"])
level = st.selectbox("Difficulty",["Beginner", "Intermediate", "Adavance"])
mode = st.radio("Activity", ["Generate questions", "Generate coding question", "Evaluate answers", "Improve answer"])
if mode == "Generate questions":
  count = st.slider("Number of Question",1,10,5)
elif mode == "Generate coding question":
  topic = st.selectbox("Topics", ["SQL", "Python", "Java", "Html", "cyber Security", "C++/C", "DSA"])
  count = st.slider("Number of Question",1,10,5)
else:
  question = st.text_area("Enter Interview Question here")
  answer = st.text_area("Enter your answer", height =160)
if st.button("Generate AI response", type = "primary"):
  if mode in ["Evaluate answers", "Improve answer"] and (not question.strip() or not answer.strip()):
    st.warning("Please enter valid question and answer")
    st.stop()
  
  if mode == "Generate questions":
    task = "Generate" + str(count) + "Generate Frequently asked intrview question not the answer only the hint"
  elif mode == "Generate coding question":
    task = "Generate" + str(count) + " Generate Frequrently asked  coding questions on topic" + topic + " and give hints to solve them. Be accurate."
  elif mode == "Evaluate answers":
    task = "Question: " + question + "My answer" + answer + " Evaluate this answer based on concept, relevance, communication, length of answer. Give each rating out of 5 in a list."
  elif mode == "Improve answer":
    task = "Question: " + question + "My answer" + answer + " Improve my answer for a better way in consice way and dont invent new thing give in a understandable way."
  background = "Job role: " + role+ "Difficulty level"+ level
  with st.spinner("Generating you answer..."):
    try:
      response = client.chat.completions.create(
        model = gen_model,
        messages = [{"role":"system",
                     "content":"Act as a Senior Interviewer,both HR and technical expert"},
                    {"role":"user",
                     "content":background + task}
                     ],
        temperature = 0.7,
        max_tokens = 1800
      )
      output = response.choices[0].message.content
      st.subheader("AI Response")
      st.markdown(output)
      st.download_button("Download Response", output , file_name = "Interview_Response.txt", mime = "text/plain")
  
    except Exception as e:
      st.error("API connection was unsucessful : ",e)
      st.info("Please check your API key and rate limits")
st.caption("Powered by streamlit.io and github using LLM API")
