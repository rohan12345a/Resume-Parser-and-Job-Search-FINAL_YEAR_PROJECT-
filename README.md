# Resume Parser Application

## Project Overview
This project aims to develop a resume parser application that extracts and highlights various entities from resumes, such as skills, job titles, and experience. These entities are categorized into specific groups and stored in the system. An API will then automatically search for relevant job opportunities on the internet and provide users with direct application links, streamlining their job search process.

## Features
- **Resume Parsing:**
  - Extracts entities such as job titles, skills, and experience.
  - Categorizes and stores extracted entities for further processing.

- **Job Search Automation:**
  - Automatically searches for job opportunities online based on the extracted data.
  - Provides direct application links to users.

- **User Interface:**
  - Allows users to upload resumes through a user-friendly interface.
  - Automatically highlights recognized entities from the uploaded resume.
  - Displays relevant job listings on the screen with direct application links.

## Dataset
- **Source:** Resumes collected from Kaggle and Google.
- **Diversity:**
  - Covers a wide range of job roles and industries.
  - Includes resumes from entry-level to experienced professionals.
  - Captures various resume formats and styles.

## Technical Details
- **Data Collection:**
  - Resumes are sourced from Kaggle and Google, ensuring diverse job roles and skill sets.

- **Text Extraction:**
  - Uses **Tesseract** and **PyPDF2** to extract text from the resumes.

- **Manual Annotation:**
  - Key job roles and skills are manually annotated by identifying keywords.

- **Named Entity Recognition (NER):**
  - NER is implemented using **SpaCy-RoBERTa** or a similar model to identify key entities.

- **Job Search Automation:**
  - Uses **Selenium** to search for job opportunities online based on the extracted entities.

- **User Interface:**
  - Built using **Streamlit** to provide an easy-to-use platform for resume uploads and job search.

## How It Works
1. Users upload a resume through the interface.
2. The application extracts key entities (skills, job titles, experience) using NER.
3. The system automatically searches for job opportunities based on the extracted entities.
4. Relevant job listings are displayed with direct links for application.

## Tools and Technologies
- **Text Extraction:** Tesseract, PyPDF2
- **NER Model:** SpaCy-RoBERTa
- **Job Search Automation:** Selenium
- **User Interface:** Streamlit

## Future Enhancements
- Expand the dataset to include more resumes from various sources.
- Improve the NER model for more accurate entity extraction.
- Integrate more job search platforms to widen job opportunities.
- Add features for personalized job recommendations based on user preferences.


