import streamlit as st
from groq import Groq                                          
st.set_page_config(page_title='AI_Interview_Assistant', page_icon='🎃', layout='centered')
st.title('🎯AI_Interview_Assistant')
st.caption('practice and perpare for your palcement here')
st.caption('Launched By Aishwarya S M')

try:
  client = Groq(api_key = ["GROQ_API_KEY"])

except(KeyError, FileNotFound): 
  st.error("API Key is missing.Add it in Advanced Setting")
  st.stop()

role = st.selectbox('Job Title', ['Machine Learning Engineer','Senior Software engineer','Devops Engineer','Data Analyst','Prompt Engineer','other'])
if role == "other":
   st.text_input("Enter you Job Title", "XXXXXXXX")
# cretar the dropdown list: two option :openai/gpt-oss-20b: openai/gpt-oss-120b
model = st.selectbox("modle", ["openai/gpt-oss-20b" ,"openai/gpt-oss-120b"])
level = st.selectbox("diffeclty", ["Beginner" ,"Intermediate","Adavance"])
mode =st.radio("Activity",["Generate Questions","Generate code Questions","evaluate Answers","Improve Answers"])
if mode == "Generate  Questions":
  count = st.slider("Number of Question",1,10,5)
elif mode == "Generate Code Questions":
  topics = st.selectbox("Topics",["SQL","DBMS","C++/C","AIML","Java","CSS","Python"])
  count = st.slider("Number of Questions",1,10,5)
else:
  Question = st.text_area("Enter Interview Question here")
  answer = st.text_area("Enter your answers",height =160)
if st.button("Generate AI Response", type = "primary"):
 if mode == (["Evaluate Answers", "Improve Answers"] and ( not question.strip() or ( not answers.strip))):
  st.warning ("Please enter a valid Question and Answer")
  st.stop()
          



