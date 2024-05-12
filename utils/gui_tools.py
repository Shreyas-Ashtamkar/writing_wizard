import streamlit as st

def show_message(content:str|dict, role:str = "user"):
    if isinstance(content, dict):
        role    = content['role']
        content = content['content']
        
    with st.chat_message(role):
        st.markdown(content)

async def stream_message(content:str|dict, role:str = "user"):
    if isinstance(content, dict):
        role    = content['role']
        content = content['content']
        
    with st.chat_message(role):
        st.write(content)
        
