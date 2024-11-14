import streamlit as st
#from langchain.chat_models import AzureChatOpenAI
#from langchain_openai import AzureChatOpenAI
#from langchain import PromptTemplate
#from langchain.chains import LLMChain
from langchain_community.chat_models import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from components.llm import llm
from dotenv import load_dotenv
load_dotenv()

def generate_answer():
    generate_button.empty()
    st.session_state.generate = True

# Set page title
st.set_page_config(
    page_title="Resource Research",
)

# Title of content
st.title("LLM Personal Trainer")
st.header("Generate Resource Suggestions")

# Initialize session state variables if they don't exist
if "generate" not in st.session_state:
    st.session_state.generate = False

if 'currentkey' not in st.session_state:
    st.session_state.currentkey = ''

AZURE_OPENAI_ENDPOINT=''
AZURE_OPENAI_DEPLOYMENT_NAME=''
AZURE_OPENAI_API_VERSION=''


# Try to get the Azure API key from secrets
try:
    st.session_state.currentkey = st.secrets["azure_openai"]["AZURE_OPENAI_API_KEY"]
    AZURE_OPENAI_ENDPOINT = st.secrets["azure_openai"]["AZURE_OPENAI_ENDPOINT"]
    AZURE_OPENAI_DEPLOYMENT_NAME = st.secrets["azure_openai"]["AZURE_OPENAI_DEPLOYMENT_NAME"]
    AZURE_OPENAI_API_VERSION = st.secrets["azure_openai"]["AZURE_OPENAI_API_VERSION"]
    st.session_state.validate = True

except KeyError:
    st.session_state.currentkey = None
    st.session_state.validate = False

# Validate API key
def validate():
    try:
        text_input = st.session_state.input
        if text_input and len(text_input) >= 32:  # Basic validation for key length
            st.session_state.currentkey = text_input
            st.session_state.validate = True
            st.sidebar.text('Azure OpenAI API key is valid')
        else:
            raise ValueError("Invalid API key format")
    except Exception as e:
        st.sidebar.text('Azure OpenAI API key not valid')

# Input for Azure API key
with st.sidebar.form('Enter Azure API key'):
    st.text_input("Enter Azure OpenAI API key", key='input')
    st.form_submit_button('Validate key', on_click=validate)

if st.session_state.currentkey:
    st.sidebar.text(f'Current Azure OpenAI API Key is valid')

    # Preference selection
    preference_list = ['Select a resource type', 'K-12 educational worksheets', 'K-12 educational videos', 'K-12 project ideas']
    option = st.selectbox('Select a preference', preference_list, placeholder='Select a preference')

    if option != 'Select a resource type':
        generate_button = st.empty()
        generate_button.button("Generate Resource Suggestions", type='primary', on_click=generate_answer)
        
        if st.session_state.generate:
            with st.spinner("Generating resource suggestions..."):
                llm = AzureChatOpenAI(
                    azure_endpoint=AZURE_OPENAI_ENDPOINT,
                    api_key=st.session_state.currentkey,
                    azure_deployment=AZURE_OPENAI_DEPLOYMENT_NAME,
                    api_version=AZURE_OPENAI_API_VERSION,
                    temperature=0.5
                )
                
                template = """
                Based on the selected preference of {preference}, provide resource suggestions.
                """
                promp = PromptTemplate(
                    input_variables=['preference'],
                    template=template
                )
                chain = LLMChain(llm=llm, prompt=promp)
                output = chain.run({'preference': option})
            st.write(output)
            st.session_state.generate = False
else:
    st.header('Enter your Azure OpenAI API key to use functionality')
