from writing_wizard import WritingWizard

import streamlit as st
from streamlit_js_eval import streamlit_js_eval

from utils.gui_tools import *

st.set_page_config(layout='wide')

st.warning("Disclaimer: This GUI is WorkInProgress.")
st.title("Writing Wizard")

with st.container(border=True):
    st.header("Article Writing")
    
    for message in WritingWizard.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    if input_ := st.chat_input("Provide a topic :"):
        WritingWizard.messages = WritingWizard.create_message( role='user', content=input_ )
        WritingWizard.messages = WritingWizard.generate_response()

with st.sidebar:
    st.title("Cool")
