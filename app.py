import os
import io
import base64
from typing import List, Dict, Optional
import streamlit as st
from dotenv import load_dotenv
import pdf2image
import google.generativeai as genai
import plotly.graph_objects as go
import PyPDF2

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

def get_gemini_response(prompt: str, resume_text: str, job_description: str) -> str:
    """Generate a response using the Gemini model."""
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(f"{prompt}\n\nResume:\n{resume_text}\n\nJob Description:\n{job_description}")
        return response.text
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return ""

def extract_text_from_pdf(uploaded_file) -> str:
    """Extract text from the uploaded PDF file."""
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text.lower()

def extract_keywords_from_response(response: str) -> Dict[str, List[str]]:
    """Extract matched and missing keywords from Gemini's response."""
    matched_keywords = []
    missing_keywords = []
    current_section = None
    for line in response.split('\n'):
        if "Most relevant matched Keywords" in line:
            current_section = "matched"
        elif "Most relevant missing Keywords" in line:
            current_section = "missing"
        elif line.strip().startswith('-') and current_section:
            keyword = line.strip()[1:].strip()
            if current_section == "matched":
                matched_keywords.append(keyword)
            elif current_section == "missing":
                missing_keywords.append(keyword)
    return {"Matched": matched_keywords, "Missing": missing_keywords}

def create_keyword_chart(keywords: Dict[str, List[str]]):
    """Create a vertical bar chart for keyword percentage comparison."""
    total_keywords = len(keywords["Matched"]) + len(keywords["Missing"])
    if total_keywords == 0:
        matched_percentage = 0
        missing_percentage = 0
    else:
        matched_percentage = len(keywords["Matched"]) / total_keywords * 100
        missing_percentage = len(keywords["Missing"]) / total_keywords * 100
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=['Keywords'],
        y=[matched_percentage],
        name='Matched',
        marker=dict(color='green')
    ))
    fig.add_trace(go.Bar(
        x=['Keywords'],
        y=[missing_percentage],
        name='Missing',
        marker=dict(color='red')
    ))
    
    fig.update_layout(
        title="Keyword Match Analysis",
        yaxis_title="Percentage of Keywords",
        xaxis_title="",
        barmode='stack',
        height=400,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    fig.add_annotation(y=matched_percentage/2, x=0, 
                       text=f"{matched_percentage:.1f}%", 
                       showarrow=False, font=dict(color="white"))
    fig.add_annotation(y=matched_percentage + missing_percentage/2, x=0, 
                       text=f"{missing_percentage:.1f}%", 
                       showarrow=False, font=dict(color="white"))
    
    fig.update_yaxes(range=[0, 100])
    
    return fig

def main():
    st.set_page_config(page_title="Resume Analyzer", layout="wide")
    st.title("Resume Analyzer")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Job Description")
        job_description = st.text_area("Enter the job description:", height=300)

    with col2:
        st.subheader("Upload Your Current Resume")
        uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

    if uploaded_file:
        st.success("Resume Uploaded Successfully")
        resume_text = extract_text_from_pdf(uploaded_file)
    else:
        resume_text = None

    if not job_description or resume_text is None:
        st.warning("Please enter a job description and upload your resume before analysis.")
    else:
        col1, col2, col3 = st.columns(3)

        with col1:
            resume_analysis = st.button("Resume Analysis", key="resume_analysis_button")
        with col2:
            keyword_analysis = st.button("Keyword Analysis", key="keyword_analysis_button")
        with col3:
            improvements = st.button("Improvements", key="improvements_button")

        if resume_analysis:
            analysis_prompt = """
            You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description.
            Please share your professional evaluation on whether the candidate's profile aligns with the role.
            Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements as follows:
            1. An overall percentage match
            2. Bullet points for strengths of the candidate relative to the job description (make the points as precise as possible)
            3. Bullet points for areas where the candidate's resume needs improvement (make the points as precise as possible)
            
            Format your response as follows:
            Resume Match Percentage: X%
            - [Resume Evaluation] (one small precise paragraph)

            Top Strengths:
            - [Strength 1]
            - [Strength 2]
            - [Strength 3]...
            (one line per strength)
            Areas for Improvement:
            - [Area 1]
            - [Area 2]
            - [Area 3]...
            (one line per Improvement)
            """
            response = get_gemini_response(analysis_prompt, resume_text, job_description)
            st.subheader("Resume Analysis")
            st.write(response)

        if keyword_analysis:
            keyword_analysis_prompt = """
            You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science, data analytics, machine learning, related technologies and other domains as well. Your task is to evaluate the provided resume against the job description.
            Please perform the following analysis:
            1. Carefully review both the job description and the resume and provide a match percentage.
            2. Identify the most important keywords mainly for technologies, skills and requirements from the job description.
            3. Determine which of these keywords and skills are present in the resume and which are missing.
            4. Calculate an overall percentage match between the resume and the job description, considering both the presence of keywords and the depth of experience or knowledge demonstrated.
            Provide your analysis in the following format:
            Keywords Match Percentage: X%
            Most relevant matched Keywords:
            - keyword1
            - keyword2
            - keyword3
            (list 5-10 most relevent matched keywords, one per line)
            Most relevant missing Keywords:
            - keyword4
            - keyword5
            - keyword6
            (list all the missing keywords one per line)
            """
            keyword_analysis_response = get_gemini_response(keyword_analysis_prompt, resume_text, job_description)
            
            st.subheader("Keyword Analysis")
            
            # Create two columns for text and chart
            col1, col2 = st.columns([6, 4])
            
            with col1:
                st.write(keyword_analysis_response)

            with col2:
                # Extract keywords from the response
                keywords = extract_keywords_from_response(keyword_analysis_response)
                
                if keywords["Matched"] or keywords["Missing"]:
                    # Create and display the keyword chart
                    fig = create_keyword_chart(keywords)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.write("No keywords extracted. Please check the response format.")

        if improvements:
            improvement_prompt = """
            Based on the job description and the candidate's current resume, provide precise and personalised tailored changes to improve the resume:
            1. List specific modifications to update the resume content (should comply with given resume).
            2. If possible, suggest exact phrasings or bullet points to add or modify the current resume.

            Format each suggestion as:
            1. specific update in resume1
            2. specific update in resume2...
            ... (continue for all suggestions)
            """
            response = get_gemini_response(improvement_prompt, resume_text, job_description)
            st.subheader("Suggested Precise Changes")
            st.write(response)

if __name__ == "__main__":
    main()
