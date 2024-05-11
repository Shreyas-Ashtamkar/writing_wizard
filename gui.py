from writing_wizard import WritingWizard

import streamlit as st
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(layout='wide')

st.warning("Disclaimer: This GUI is WorkInProgress.")
st.title("Writing Wizard")

with st.container(border=True):
    st.header("Article Writing")
    if input := st.chat_input("Provide a topic :"):
        WritingWizard.chat(input)
        
    with st.container(border=False):
        for message in WritingWizard.messages:
            with st.chat_message(message['role']):
                st.markdown(message['content'])
    

with st.sidebar:
    st.title("Cool")
