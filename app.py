import streamlit as st
from agents.video_agent import initialize_agent , analyze_video_agent
from utils.file_utils import save_temp_files
from config.config import configure_env

from pathlib import Path
import os 

configure_env()

st.set_page_config(page_title="Video Chat AI" , page_icon="🎥" , layout="wide")
st.title("🎥 AI Chat with videos ") 
st.caption("Gemini 2.0 & Phi Agent ")

st.sidebar.header("upload video")
video_files = st.sidebar.file_uploader("upload a video" , type= ["mp4" , "avi"])


video_path =None
if video_files :
    video_path= save_temp_files(video_files)
    st.sidebar.success("video uploaded successfuly")

if "chat_history" not in st.session_state :
    st.session_state.chat_history = []

if "agent" not in st.session_state:
    st.session_state.agent = initialize_agent()



if video_files and video_path : 
    st.subheader("chat with the video ")
    user_input = st.chat_input("ask something about the video")

    if user_input :
        st.session_state.chat_history.append({"role" : "user" , "content" : user_input})

        with st.spinner("analyzing video ..."):
            try:
                response = analyze_video_agent(st.session_state.agent , video_path , user_input)
                st.session_state.chat_history.append({"role" : "analyst" , "content" : response})
            except Exception as e :
                error_msg= f"Error : {e}"
                st.session_state.chat_history.append({"role" : "analyst" ,"content" : error_msg}) 


    for msg in st.session_state.chat_history :
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    if st.sidebar.button("clear chat") :
        st.session_state.chat_history = []
        if video_path :
            Path(video_path).unlink(missing_ok=True)
        st.rerun()
else : 
    st.info("upload a video for conversation")