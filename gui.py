from writing_wizard import WritingWizard

import streamlit as st
from utils.gui_tools import *

import pyperclip

st.set_page_config(layout='wide')

st.warning("Disclaimer: This GUI is WorkInProgress.")
st.title("Writing Wizard")

with st.container(border=True):
    st.header("Article Writing")
    
    for message in WritingWizard.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    if input_ := st.chat_input("Provide a topic :"):
        WritingWizard.clear_messages()
        
        WritingWizard.messages = WritingWizard.create_message( role='user', content=input_ )
        show_message(WritingWizard.last_message)
        
        WritingWizard.messages = WritingWizard.generate_response()
        show_message(WritingWizard.last_message)
    
    if WritingWizard.last_message:
        st.button(
            label    = "Copy to Clipboard",
            on_click = pyperclip.copy( WritingWizard.last_message['content'] )
        )

# with st.sidebar:
#     st.title("Cool")
