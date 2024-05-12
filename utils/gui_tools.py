import streamlit as st

def show_message(content:str|dict, role:str = "user"):
    """Show a message in the chat with the specified role.
    
    Args:
        content (str | dict): The content of the message to be displayed. If a dictionary is provided, it should have keys 'role' and 'content'.
        role (str, optional): The role of the message sender. Defaults to "user".
    """
    if isinstance(content, dict):
        role    = content['role']
        content = content['content']
        
    with st.chat_message(role):
        st.markdown(content)

async def stream_message(content:str|dict, role:str = "user"):
    """Asynchronously streams a message with the specified content and role.
    
    Args:
        content (str | dict): The content of the message to be streamed. If a dictionary is provided, it should have 'role' and 'content' keys.
        role (str, optional): The role of the message sender. Defaults to "user".
    """
    if isinstance(content, dict):
        role    = content['role']
        content = content['content']
        
    with st.chat_message(role):
        st.write(content)
        
