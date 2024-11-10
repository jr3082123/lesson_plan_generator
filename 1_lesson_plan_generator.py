import streamlit as st
from langchain.chat_models import AzureChatOpenAI  # Updated import
from langchain import PromptTemplate
from langchain.chains import LLMChain
from components.llm import llm
import os
from fpdf import FPDF
import io

def generate_program():
    st.session_state.generate = True

# Set page title
st.set_page_config(
    page_title="Lesson Plan Generator",
)

# Title of content
st.title("LLM Lesson Plan Assistant")
st.header("Lesson Plan Generator")

# Initialise session state variables if they don't exist
if "generate" not in st.session_state:
    st.session_state.generate = False

if 'currentkey' not in st.session_state:
    st.session_state.currentkey = ''

# Retrieve Azure OpenAI configurations
AZURE_OPENAI_API_KEY = st.session_state.currentkey
AZURE_OPENAI_DEPLOYMENT_NAME = "gpt-35-turbo-16k"  # Set your Azure deployment name
AZURE_ENDPOINT = "https://mylessonservice.openai.azure.com/"  # Set your Azure endpoint
API_VERSION = "2024-08-01-preview"  # Use the correct API version

if 'validate' not in st.session_state:
    st.session_state.validate = False

if 'validate_count' not in st.session_state:
    st.session_state.validate_count = 0

# Try to get the Azure API key from secrets
try:
    st.session_state.currentkey = os.environ.get('AZURE_OPENAI_API_KEY')
except:
    pass

# Function to validate the Azure key
def validate():
    try:
        text_input = st.session_state.input
        # Set the API key for validation
        st.session_state.validate_count += 1
        st.session_state.currentkey = text_input
        st.session_state.validate = False
    except:
        st.sidebar.text('Azure OpenAI API key not valid')

with st.sidebar.form('Enter Azure API key'):
    st.text_input("Enter Azure OpenAI API key", key='input')
    st.form_submit_button('Validate key', on_click=validate)

if st.session_state.currentkey:
    st.sidebar.text('Current Azure OpenAI API Key is valid')

if st.session_state.currentkey:
    
    # Student Demographics
    st.header("Student Demographics")
    name = st.text_input("Name")
    
    grades = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th"]
    age_group = st.selectbox("Select Age Group", ["6-10", "11-14", "15-18"])
    grade_level = []
    grade = "elementary"
    if age_group == "6-10":
        grade_level = st.selectbox("Select Grade Level", grades[0:5])
    elif age_group == "11-14":
        grade_level = st.selectbox("Select Grade Level", grades[5:8])
        grade = "middle"
    else:
        grade_level = st.selectbox("Select Grade Level", grades[8:])
        grade = "high"
    
    specific_needs = st.radio("Identify Specific Needs", ['None', 'Dyslexia', 'Dyscalculia','Dysgraphia','Speeh Impairment','Emotional Disturbance', 'ASD', 'ADHD'], index=0)

    # Learning Goals
    st.header("Learning Goals")
    st.write(f"Lesson Plan will use the Texas Essential Knowledge and Skill categories based on the Grade Level and Subject Area you choose.")
    
    # Difficulty Level
    col1, col2 = st.columns(2)
    difficulty_level = col1.select_slider("Select the difficulty level for goals", options=["Low", "Medium", "High"])

    # Preferred Teaching Methods
    st.header("Preferred Teaching Methods")
    teaching_methods = st.multiselect("Select Preferred Teaching Methods", 
                                       ["Direct Instruction", "Cooperative Learning", "Project-Based Learning"])

    # Customization Options
    st.header("Customization Options")

    # Lesson Type
    lesson_type = st.selectbox("Select Lesson Type", ["Inquiry-Based", "Direct Instruction", "Collaborative"])
    
    # Lesson Length
    lesson_length = st.slider("Select Duration of the Lesson (in minutes)", 30, 120, 60)

    # Subject Matter
    subject_area = st.selectbox("Choose Subject Area", ["Math", "Science", "Language Arts"])

    learning_standards = f"grade level {grade_level} and subject area {subject_area}"
    
    # Define specific topics based on subject area
    if subject_area == "Math":
        if grade == 'elementary':
            specific_topics = st.multiselect("Select Specific Topics", ["Counting and Cardinality", "Operations and Algebraic Thinking", "Number and Operations in Base Ten","Measurement and Data","Geometry"])
        elif grade == "middle":
            specific_topics = st.multiselect("Select Specific Topics", ["Ratios and Proportional Relationships", "The Number System", "Expressions and Equations","Geometry","Statistics and Probability"])
        else:
            specific_topics = st.multiselect("Select Specific Topics", ["Algebra", "Geometry", "Trigonometry","Statistics and Probability","Calculus"])

    elif subject_area == "Science":
         if grade == "elementary" or grade == "middle":
            specific_topics = st.multiselect("Select Specific Topics", ["Life Science", "Physical Science", "Earth Science","Space Science","Environmental Science"])
         else:
            specific_topics = st.multiselect("Select Specific Topics", ["Biology", "Chemistry", "Physics","Earth and Space Science","Environmental Science"])
        
    elif subject_area == "Language Arts":
        specific_topics = st.multiselect("Select Specific Topics", ["Grammar", "Literature", "Writing"])
    else:
        specific_topics = st.multiselect("Select Specific Topics", [])

    if st.button("Generate Program", on_click=generate_program):
        st.session_state.generate = True

    if st.session_state.generate:
        with st.spinner("Generating program..."):
            output_concat = ""

            # Updated template for the first week
            template = """
            Create a tailored lesson plan for {name} based on (Age Group: {age_group}, Grade Level: {grade_level}, Specific Needs: {specific_needs}) and the following details:

            Learning Standards: {learning_standards}
            Difficulty Level: {difficulty_level}
            Preferred Teaching Methods: {teaching_methods}
            Lesson Type: {lesson_type}
            Lesson Length: {lesson_length} minutes
            Subject Area: {subject_area}
            Specific Topics: {specific_topics}
            """

            promp = PromptTemplate(
                input_variables=['name', 'age_group', 'grade_level','specific_needs',
                                 'learning_standards', 'difficulty_level', 'teaching_methods', 
                                 'lesson_type', 'lesson_length', 'subject_area', 
                                 'specific_topics'],
                template=template
            )

            chain = LLMChain(llm=llm, prompt=promp)
            output = chain.run({
                'name': name,
                'age_group': age_group,
                'grade_level': grade_level,
                'specific_needs':{specific_needs},
                'learning_standards': learning_standards,
                'difficulty_level': difficulty_level,
                'teaching_methods': ", ".join(teaching_methods),
                'lesson_type': lesson_type,
                'lesson_length': lesson_length,
                'subject_area': subject_area,
                'specific_topics': ", ".join(specific_topics)
            })
            st.write(output)
            output_concat += output

            # Generate PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=10)  # Set font size

           # Set the width of the cell to avoid text going off the page
            page_width = pdf.w - 2 * pdf.l_margin

            # Check if there is any content to print
            if output_concat.strip():
                lines = output_concat.splitlines()

                line_height = 5  # Adjust line spacing as needed

                for line in lines:
                    pdf.write(line_height, line)
                    pdf.ln(line_height)  # Move cursor to the next line
            else:
                pdf.cell(page_width, 10, txt="Error: No content generated.")


            # Save PDF as bytes
            pdf_output = pdf.output(dest='S')  # This returns a bytearray
            pdf_buffer = io.BytesIO(pdf_output)

            # Provide download button
            st.download_button(
                label="Download Lesson Plan as PDF",
                data=pdf_buffer,
                file_name="lesson_plan.pdf",
                mime="application/pdf"
            )
        
          

            # Reset generate flag after downloading
            st.session_state.generate = False
else:
    st.header('Enter your Azure OpenAI API key to use functionality')