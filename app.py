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
gen_model = st.selectbox("modle", ["openai/gpt-oss-20b" ,"openai/gpt-oss-120b"])
level = st.selectbox("diffeclty", ["Beginner" ,"Intermediate","Adavance"])
mode =st.radio("Activity",["Generate Questions","Generate code Questions","Evaluate Answers","Improve Answers"])
if mode == "Generate  Questions":
  count = st.slider("Number of Question",1,10,5)
elif mode == "Generate Code Questions":
  topics = st.selectbox("Topics",["SQL","DBMS","C++/C","AIML","Java","CSS","Python"])
  count = st.slider("Number of Questions",1,10,5)
else:
  Question = st.text_area("Enter Interview Question here")
  answer = st.text_area("Enter your answers",height =160)
if st.button("Generate AI Response", type = "primary"): 
 if mode in ["Evaluate Answers", "Improve Answers"] and ( not question.strip() or not answers.strip()):
  st.warning ("Please enter a valid Question and Answer")
  st.stop()
   
if mode == "Generate  Questions":
  task = "Generate" + str(count) + "Frequently asked Interview Questions, 3 theory and 2 scenario questions.Do not give answers. Give the hint"
elif mode == "Generate Code Questions":
  task = "Generate" + str(count) + "Frequently asked coding questions on topic" + topic +"and give hints to solve them. Be accurate."
elif mode == "Evaluate Answers":
   task = "Question :" + question +"My answer : " + answer + " Evaluate this answers based on concept, relevance, communication, length of answer .G ive each rating out of  5 in the list."
elif mode == "Improve Answers":
   task = "Question :" + question +"My answer : " + answer + " Improve my answer and give the correct answer in simple English." 
background = "Job role :" + role + " Difficulti level " + level 
with st.spinner ("Genrating your answer ...."):
  try:
    response = client .chat.completions.create(
      model = gen_model,
      messages = [{"role":"system",
                   "content":"Act as a Senior Interviwer, both HR and Technical expert"},
                  {"role" : "user",
                   "content" : background + task }],
      temperature = 0.7,
      max_tokens = 1800 )
    output =  response.choices[0].message.content
    st.subheader("AI Response")
    st.markdown(output)
    st.download_button("Download Response", output , file_name ="Interview_Response.txt", mime = "text/plain")
  
  except Exception as e:
    st.error ("API connection was unsuccessful")
    st.info("Please check your API key and rate limits")
st.caption("Powered by Streamlit.io and Github. Using LLM API")
