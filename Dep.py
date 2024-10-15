
import spacy
import streamlit as st
import PyPDF2
import pandas as pd
import plotly.express as px
import google.generativeai as genai  # Import Google Generative AI
import http.client
import json
from spacy import displacy
from streamlit_lottie import st_lottie  # Import Lottie package
import requests  # To fetch the Lottie animation

# Function to load Lottie animation
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

# Load Lottie animation
lottie_animation = load_lottie_url("https://lottie.host/10ef4447-c72d-44b4-b562-c93542913924/rQXGHy5QwU.json")

# Configure Google Generative AI
GOOGLE_API_KEY = 'AIzaSyCByDN630R0xn5_wXh4GgZBhBqX3Nw8S90'  # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)

# Function to extract text from PDF using PdfReader (PyPDF2 3.x)
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

# Load the SpaCy model from the 'model-last' folder
@st.cache_resource
def load_spacy_model():
    model_path = "C:/Users/Lenovo/Downloads/model-last"  # Replace with your actual model path
    nlp = spacy.load(model_path)  # This will load the model based on 'config.cfg'
    return nlp

# Function to visualize named entities in color
def visualize_entities(doc):
    colors = {
        "SKILLS": "linear-gradient(90deg, #aa9cfc, #fc9ce7)",
        "JOB TITLE": "linear-gradient(90deg, #9BE15D, #00E3AE)",
        "ORGANIZATION": "#ffd966",
        "EDUCATION": "#9fc5e8",
        "EXPERIENCE": "#9fc9e8",
        "DATE": "#9fc5e8"
    }
    options = {
        "ents": ["JOB TITLE", "SKILLS", "ORGANIZATION", "EDUCATION", "EXPERIENCE", "DATE"],
        "colors": colors
    }
    html = displacy.render(doc, style="ent", options=options)
    html = html.replace("\n", "")
    st.write(html, unsafe_allow_html=True)

# Function to create sunburst visualization
def create_sunburst(entities):
    data = [{'Category': ent[1], 'Value': ent[0]} for ent in entities]
    df = pd.DataFrame(data)
    fig = px.sunburst(df, path=['Category', 'Value'])
    fig.update_layout(title="Resume Overview: Key Information Extracted")
    st.plotly_chart(fig)



# Function to get job roles from Google Gemini AI using skills (limited to top 5)
def get_job_roles_from_gemini(skills):
    prompt = "Provide relevant job roles based on the following skills:\n" + ", ".join(skills)
    llm_model = genai.GenerativeModel('gemini-pro')
    response = llm_model.generate_content(prompt)
    return response.text.strip()

# Function to search for jobs based on job role and location
def search_jobs(job_roles, job_location):
    conn = http.client.HTTPSConnection("jobs-search-api.p.rapidapi.com")
    payload = f'{{"search_term":"{job_roles}","location":"{job_location}","results_wanted":5,"site_name":["indeed","linkedin","zip_recruiter","glassdoor"],"distance":50,"job_type":"fulltime","is_remote":false,"linkedin_fetch_description":false,"hours_old":72}}'
    headers = {
        'x-rapidapi-key': "1a20cedd60msh43d38c1f42ba976p12bf72jsndf09cdb52f10",
        'x-rapidapi-host': "jobs-search-api.p.rapidapi.com",
        'Content-Type': "application/json"
    }
    conn.request("POST", "/getjobs", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))

# Streamlit UI
st.title("AI-Powered Resume Parser and Job Finder")

# Load and display Lottie animation
st_lottie(lottie_animation, speed=1, height=200, width=200, key="initial")

# Step 1: Upload PDF and Extract Text
st.header("Step 1: Upload Your Resume")
st.info("Upload your resume in PDF format to extract named entities like skills, job titles, etc.")

pdf_file = st.file_uploader("Choose a PDF file", type="pdf")

if pdf_file and st.button("Extract Information from Resume"):
    st.write("Processing your resume... Please wait.")
    resume_text = extract_text_from_pdf(pdf_file)
    nlp = load_spacy_model()
    doc = nlp(resume_text)

    # Show extracted entities with color highlighting
    st.subheader("Extracted Information")
    visualize_entities(doc)

    # Save extracted entities for next steps
    extracted_entities = [(ent.text, ent.label_) for ent in doc.ents]
    st.session_state['extracted_entities'] = extracted_entities

    # Display sunburst chart of entities
    st.subheader("Resume Overview: Visual Breakdown")
    create_sunburst(extracted_entities)

# Step 2: Generate Job Roles Based on Extracted Skills
if 'extracted_entities' in st.session_state and st.button("Generate Relevant Job Roles Based on Skills"):
    st.write("Extracting the top 5 skills from your resume and generating relevant job roles...")

    # Extract only top 5 skills
    extracted_skills = [ent[0] for ent in st.session_state['extracted_entities'] if ent[1] == "SKILLS"][:5]

    # Ensure there are enough skills to proceed
    if extracted_skills:
        # Generate job roles using Google Gemini AI
        try:
            job_roles = get_job_roles_from_gemini(extracted_skills)
            st.subheader("AI-Generated Job Roles")
            st.write("Based on your skills, here are some relevant job roles you can consider:")
            st.write(job_roles)
            st.session_state['job_roles'] = job_roles
        except Exception as e:
            st.error(f"Error generating job roles: {e}")
    else:
        st.error("No skills detected in your resume. Please ensure that your resume includes a section for skills.")

# Step 3: Job Search Interface
if 'job_roles' in st.session_state:
    st.header("Step 3: Find Jobs Based on Your Skills")
    job_roles_input = st.text_input("Job Role", value=st.session_state.get('job_roles', ''),
                                     help="You can edit the suggested job role or enter your own.")
    job_location_input = st.text_input("Location", value=st.session_state.get('job_location', ''),
                                        help="Enter the city or region where you want to find jobs.")

    # Store the job role and location in session state
    if job_roles_input:
        st.session_state['job_roles'] = job_roles_input
    if job_location_input:
        st.session_state['job_location'] = job_location_input

    if st.button("Search for Jobs"):
        if job_roles_input and job_location_input:
            st.write("Searching for job opportunities... Please wait.")
            job_results = search_jobs(job_roles_input, job_location_input)

            if 'jobs' in job_results and job_results['jobs']:
                st.subheader(f"Job Listings for '{job_roles_input}' in '{job_location_input}':")
                for job in job_results['jobs']:
                    # Customize the styles for job title and company
                    job_title = f"<span style='color: #1E90FF; font-weight: bold;'>{job['title']}</span>"
                    company_name = f"<span style='color: #FF4500; font-weight: bold;'>{job['company']}</span>"

                    st.markdown(f"**Job Title:** {job_title}", unsafe_allow_html=True)
                    st.markdown(f"**Company:** {company_name}", unsafe_allow_html=True)
                    st.markdown(f"**Location:** {job['location']}")
                    st.markdown(f"[Job URL]({job['job_url']})")
                    st.markdown(f"**Date Posted:** {job['date_posted'] if job['date_posted'] else 'Not specified'}")
                    st.markdown("---")
            else:
                st.write("No job listings found for your search criteria.")
        else:
            st.error("Please enter both a job role and a location.")

with st.container():
    with st.sidebar:
        members = [
            {"name": "Rohan Saraswat", "email": "rohan.saraswat2003@gmail. com", "linkedin": "https://www.linkedin.com/in/rohan-saraswat-a70a2b225/"},
            {"name": "Saksham Jain", "email": "sakshamgr8online@gmail. com", "linkedin": "https://www.linkedin.com/in/saksham-jain-59b2241a4/"},
            {"name": "Shambhavi Kadam", "email": "shambhavi.kadam.btech2021@sitpune.edu.in",
             "linkedin": "https://www.linkedin.com/in/shambhavi-kadam-63157a1a1/"},
            {"name": "Rishit Jain", "email": "rishit.jain.btech2021@sitpune.edu.in",
             "linkedin": "https://www.linkedin.com/in/rishit-jain-849471230/"},
        ]

        # Define the page title and heading
        st.markdown("<h1 style='font-size:28px'>Authors</h1>", unsafe_allow_html=True)

        # Iterate over the list of members and display their details
        for member in members:
            st.write(f"Name: {member['name']}")
            st.write(f"Email: {member['email']}")
            st.write(f"LinkedIn: {member['linkedin']}")
            st.write("")


