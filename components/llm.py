import os
import streamlit as st
#from langchain_openai import AzureChatOpenAI
#from langchain.chat_models import AzureChatOpenAI
from langchain_community.chat_models import AzureChatOpenAI

from dotenv import load_dotenv

load_dotenv()

try:
    AZURE_OPENAI_API_KEY = os.environ.get('AZURE_OPENAI_API_KEY')
    AZURE_OPENAI_DEPLOYMENT_NAME = os.environ.get('AZURE_OPENAI_DEPLOYMENT_NAME')
    AZURE_OPENAI_ENDPOINT = os.environ.get('AZURE_OPENAI_ENDPOINT')
    AZURE_OPENAI_API_VERSION = os.environ.get('AZURE_OPENAI_API_VERSION')
except:
    try:
        AZURE_OPENAI_API_KEY = st.secrets["azure_openai"]["AZURE_OPENAI_API_KEY"]
        AZURE_OPENAI_ENDPOINT = st.secrets["azure_openai"]["AZURE_OPENAI_ENDPOINT"]
        AZURE_OPENAI_DEPLOYMENT_NAME = st.secrets["azure_openai"]["AZURE_OPENAI_DEPLOYMENT_NAME"]
        AZURE_OPENAI_API_VERSION = st.secrets["azure_openai"]["AZURE_OPENAI_API_VERSION"]

    except KeyError:
        st.session_state.currentkey = None
        st.session_state.validate = False

    
llm = AzureChatOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_KEY=AZURE_OPENAI_API_KEY,
    azure_deployment=AZURE_OPENAI_DEPLOYMENT_NAME,
    api_version=AZURE_OPENAI_API_VERSION,
    temperature=0,
    streaming=True
)