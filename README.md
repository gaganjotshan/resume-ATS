# Resume Application Tracking System (ATS)

## Overview
This project is an End-to-End Resume (ATS) Analyzer designed to help candidates evaluate their resumes against job descriptions using the Google Gemini Pro Vision AI Model. It automates the resume scoring process to provide candidates with insights into their application's suitability.

## Features
- Upload and analyze PDF resumes
- Input job descriptions for comparison
- Get detailed feedback on resume-job alignment
- Calculate percentage match between resume and job requirements
- Identify missing keywords and skills
- Automated feedback with actionable insights on resume improvements
- Intuitive user interface for easy interaction

## Technologies Used
- **Google Gemini Pro Vision AI Model**: Utilized for resume parsing and analysis
- **Backend**: Python, Streamlit
- **Frontend**: Streamlit
- **Cloud Services**: Google Cloud Platform (GCP) for API integration
- **Additional Libraries**: pdf2image, python-dotenv, Pillow

## High-Level Diagram
[User] --> [Streamlit Frontend]
[Streamlit Frontend] --> [Python Backend]
[Python Backend] --> [PDF Processor]
[Python Backend] --> [Keyword Analyzer]
[Python Backend] --> [Gemini AI Model]
[Python Backend] --> [Visualization Engine]
[Visualization Engine] --> [Streamlit Frontend]

## Installation

### Prerequisites
- Python 3.7+
- pip
- Google Cloud account with Gemini API access

### Setup
1. Clone the repository:
```
git clone https://github.com/yourusername/resume-ATS.git
cd resume-ATS
```

2. Install required packages:
```
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory and add your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```


## Usage
1. Run the Streamlit app:
```
streamlit run app.py
```


2. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Use the interface to:
- Enter a job description
- Upload a resume PDF
- Click on analysis buttons to get insights

## How It Works
1. The app uses `pdf2image` to convert uploaded PDFs to images.
2. Google's Gemini Pro Vision model analyzes the resume image and job description.
3. AI-generated insights are presented based on the selected analysis type.

## Functionalities
- Input field for job descriptions
- Resume PDF upload
- PDF to image conversion and processing with Google Gemini Pro
- Multiple prompts template for different types of analysis

## Dependencies
- streamlit
- google-generativeai
- pdf2image
- python-dotenv
- Pillow

## Configuration
Ensure your Google API key is correctly set in the `.env` file for the application to function properly.

## Contributing
Contributions to improve the ATS Resume Expert are welcome. Please follow these steps:
1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## Acknowledgements
- [Google Gemini AI](https://ai.google.dev/)
- [Streamlit](https://streamlit.io/)
- [pdf2image](https://github.com/Belval/pdf2image)
