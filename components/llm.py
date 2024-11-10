import os
import streamlit as st
from langchain_community.chat_models import AzureChatOpenAI
from dotenv import load_dotenv

# Load environment variables if they exist
load_dotenv()

# Attempt to retrieve credentials from environment variables
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

# Fallback to Streamlit secrets if environment variables are missing
if not AZURE_OPENAI_API_KEY or not AZURE_OPENAI_DEPLOYMENT_NAME or not AZURE_ENDPOINT or not API_VERSION:
    try:
        AZURE_OPENAI_API_KEY = st.secrets["azure_openai"]["AZURE_OPENAI_API_KEY"]
        AZURE_ENDPOINT = st.secrets["azure_openai"]["AZURE_OPENAI_ENDPOINT"]
        AZURE_OPENAI_DEPLOYMENT_NAME = st.secrets["azure_openai"]["AZURE_OPENAI_DEPLOYMENT_NAME"]
        API_VERSION = st.secrets["azure_openai"]["AZURE_OPENAI_API_VERSION"]
    except KeyError as e:
        st.error(f"Missing configuration in secrets.toml: {e}")
        st.stop()

# Ensure all required values are set
if not all([AZURE_OPENAI_API_KEY, AZURE_ENDPOINT, AZURE_OPENAI_DEPLOYMENT_NAME, API_VERSION]):
    st.error("Azure OpenAI API credentials are incomplete. Please check environment variables or secrets.toml.")
    st.stop()

# Initialize AzureChatOpenAI if all credentials are present
try:
    llm = AzureChatOpenAI(
        azure_endpoint=AZURE_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        azure_deployment=AZURE_OPENAI_DEPLOYMENT_NAME,
        api_version=API_VERSION,
        temperature=0,
        streaming=True
    )
except Exception as e:
    st.error(f"Failed to initialize AzureChatOpenAI: {e}")
