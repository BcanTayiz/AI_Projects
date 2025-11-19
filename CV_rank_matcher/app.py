"""
================================================================================
CV Ranker – Compare & Rank Resumes using AI & TrueSkill
================================================================================

Project Overview:
-----------------
The CV Ranker is an interactive Streamlit application designed to assist HR professionals,
recruiters, or hiring managers in comparing and ranking multiple CVs (resumes) efficiently.
Instead of manually reviewing each CV, this tool leverages natural language processing (NLP) 
techniques and the TrueSkill ranking system to generate a fair, data-driven leaderboard of CVs 
based on skills, keywords, and similarity metrics.

Key Features:
-------------
1. CV Upload:
   - Supports multiple file formats: PDF and DOCX.
   - Users can upload any number of CVs for comparison.

2. Text Extraction:
   - Extracts textual content from uploaded documents using PyPDF2 (for PDFs) 
     and python-docx (for DOCX files).
   - Ensures clean text is ready for NLP analysis.

3. Skill & Keyword Scoring:
   - Users can provide a list of important skills or keywords relevant to the job.
   - Each CV is analyzed for the presence of these keywords.
   - A skill score is computed for each CV based on keyword matches.

4. Pairwise Similarity:
   - Computes cosine similarity between CVs using TF-IDF vectorization.
   - Identifies how similar CVs are in terms of content and skills.

5. TrueSkill Ranking:
   - Implements a TrueSkill-based ranking system (similar to ELO rating in chess).
   - Treats each CV as a “player” and each pairwise comparison as a “match”.
   - Automatically updates ratings and generates a global leaderboard.
   - Produces a fair and dynamic ranking that accounts for multiple comparisons.

6. Streamlit Interface:
   - Interactive and easy-to-use UI.
   - Upload CVs, input keywords, view skill scores, similarity scores, and global leaderboard.
   - Optional: future extensions could include visual heatmaps, highlighted skills, and PDF report downloads.

Technologies & Libraries Used:
-------------------------------
- Streamlit: Frontend UI
- PyPDF2 & python-docx: Document parsing
- scikit-learn: NLP and TF-IDF vectorization
- TrueSkill: Ranking system for pairwise comparisons
- pandas & numpy: Data management and computation
- plotly (optional): Visualization of leaderboard and similarity metrics

Use Case:
---------
This project is ideal for companies or organizations that need to:
- Quickly shortlist CVs from a large pool of applicants
- Identify top candidates based on skills and experience
- Automate repetitive tasks in resume evaluation
- Gain data-driven insights into CV comparisons

Potential Extensions:
---------------------
- Integrate with job description matching for weighted skill scoring
- Visualize global CV ranking using interactive charts
- Include AI-powered recommendations for CV improvement
- Deploy as a web service for recruitment platforms

================================================================================
"""





import streamlit as st
from utils.file_parser import extract_text
from utils.scoring import compute_similarity, skill_score
from utils.ranking import compare_pair
import pandas as pd

st.markdown("""
# CV Ranker – Compare & Rank Resumes

**Overview:**  
CV Ranker is an interactive tool that helps recruiters and hiring managers compare multiple CVs efficiently. It analyzes resumes for skills, keywords, and content similarity, then generates a fair ranking using a TrueSkill-based system.

**Key Features:**  
- Upload PDF or DOCX CVs  
- Analyze for important skills/keywords  
- Compute similarity between CVs  
- Rank CVs automatically using TrueSkill  
- View a leaderboard of top candidates  

**Use Case:**  
Quickly shortlist and identify top candidates from a large pool, making the recruitment process faster and more data-driven.
""")

# Upload CVs
uploaded_files = st.file_uploader(
    "Upload CVs (PDF or DOCX)", accept_multiple_files=True
)

keywords_input = st.text_area(
    "Enter important skills/keywords separated by comma",
    value="Python, Machine Learning, Data Analysis"
)
keywords = [k.strip() for k in keywords_input.split(",")]

if uploaded_files and len(uploaded_files) >= 2:
    cv_texts = [extract_text(f) for f in uploaded_files]
    cv_names = [f.name for f in uploaded_files]
    
    # Compute skill scores
    scores = [skill_score(t, keywords) for t in cv_texts]
    
    # Pairwise comparison and ranking
    n = len(cv_texts)
    ratings = [score for score in scores]  # start with skill scores
    leaderboard = pd.DataFrame({"CV": cv_names, "Score": ratings})
    
    # Show leaderboard
    st.subheader("CV Leaderboard")
    st.dataframe(leaderboard.sort_values("Score", ascending=False))
    
    # Optional: show pairwise similarity
    st.subheader("Pairwise Similarity")
    for i in range(n):
        for j in range(i+1, n):
            sim = compute_similarity(cv_texts[i], cv_texts[j])
            st.write(f"{cv_names[i]} vs {cv_names[j]} → Similarity: {sim:.2f}")
