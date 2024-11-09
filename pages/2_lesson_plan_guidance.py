import streamlit as st
#from langchain.chat_models import AzureChatOpenAI
#from langchain import PromptTemplate
#from langchain.chains import LLMChain
from langchain_community.chat_models import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
import json
import requests

def generate_answer():
    generate_button.empty()
    st.session_state.generate = True

# Load fitness questions
with open('questions.json', 'r') as json_file:
    json_data = json_file.read()
    data = json.loads(json_data)

# Set page title
st.set_page_config(
    page_title="Lesson Plan Guidance Questions",
)

# Title of content
st.title("LLM Lesson Plan Assistant")
st.header("Lesson Plan Guidance Questions")

# Initialize the session states if they don't exist
if "generate" not in st.session_state:
    st.session_state.generate = False

if 'currentkey' not in st.session_state:
    st.session_state.currentkey = ''

# Retrieve Azure OpenAI configurations
AZURE_OPENAI_API_KEY = st.session_state.currentkey
AZURE_OPENAI_DEPLOYMENT_NAME = "gpt-35-turbo-16k"  # Set your Azure deployment name
AZURE_ENDPOINT = "https://mylessonservice.openai.azure.com/"  # Set your Azure endpoint
API_VERSION = "2024-08-01-preview"  # Use the correct API version


questions = data['questions']
question_list = []


def validate():
    try:
        text_input = st.session_state.input
        
        # Basic validation: Check if the key is not empty and has a reasonable length
        if text_input and len(text_input) >= 32:  # Adjust length based on your key's expected length
            st.session_state.currentkey = text_input
            st.session_state.validate = True
            st.sidebar.text('Azure OpenAI API key is valid')
        else:
            raise ValueError("Invalid API key format")

    except Exception as e:
        st.sidebar.text('Azure OpenAI API key not valid')


with st.sidebar.form('Enter Azure API key'):
    st.text_input("Enter Azure OpenAI API key", key='input')
    st.form_submit_button('Validate key', on_click=validate)

if st.session_state.currentkey:
    side_text = st.sidebar.text(f'Current Azure OpenAI API Key is valid')

if st.session_state.currentkey:
    question_list.append('Select a question')
    for question in questions:
        question_list.append(question['question'])

    option = st.selectbox('Select a question', question_list, placeholder='Select a question')

    if option != 'Select a question':
        generate_button = st.empty()
        generate_button.button("Generate Answer", type='primary', on_click=generate_answer)
        if st.session_state.generate:
            with st.spinner("Answering your question..."):
                llm = AzureChatOpenAI(
                    azure_endpoint=AZURE_ENDPOINT,
                    api_key=st.session_state.currentkey,
                    azure_deployment=AZURE_OPENAI_DEPLOYMENT_NAME,
                    api_version=API_VERSION,
                    temperature=0.5
                )
                template = """
                {option}
                """
                promp = PromptTemplate(
                    input_variables=['option'],
                    template=template
                )
                chain = LLMChain(llm=llm, prompt=promp)
                output = chain.run({'option': option})
            st.write(output)
            st.session_state.generate = False
else:
    st.header('Enter your Azure OpenAI API key to use functionality')