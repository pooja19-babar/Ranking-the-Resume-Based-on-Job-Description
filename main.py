# # import os
# # import re
# # import docx2txt
# # import PyPDF2
# # from sentence_transformers import SentenceTransformer, util
# # import spacy
# # import pandas as pd

# # # -------------------------------
# # # Load models
# # # -------------------------------
# # embedder = SentenceTransformer('all-MiniLM-L6-v2')
# # nlp = spacy.load("en_core_web_sm")

# # # -------------------------------
# # # Helper functions
# # # -------------------------------
# # def extract_text(file_path):
# #     """Extract text from PDF or DOCX."""
# #     text = ""
# #     if file_path.endswith(".pdf"):
# #         with open(file_path, "rb") as f:
# #             reader = PyPDF2.PdfReader(f)
# #             for page in reader.pages:
# #                 text += page.extract_text() + "\n"
# #     elif file_path.endswith(".docx"):
# #         text = docx2txt.process(file_path)
# #     elif file_path.endswith(".txt"):
# #         with open(file_path, "r", encoding="utf-8") as f:
# #             text = f.read()
# #     return text

# # def clean_text(text):
# #     """Basic text cleaning."""
# #     return re.sub(r'[^a-zA-Z0-9 ]', ' ', text.lower())

# # def extract_skills(text, jd_skills):
# #     """Check which JD skills are present in resume."""
# #     resume_tokens = set(clean_text(text).split())
# #     matched = [skill for skill in jd_skills if skill.lower() in resume_tokens]
# #     missing = [skill for skill in jd_skills if skill.lower() not in resume_tokens]
# #     return matched, missing

# # def compute_similarity(jd_text, resume_text):
# #     """Semantic similarity using embeddings."""
# #     jd_emb = embedder.encode(jd_text, convert_to_tensor=True)
# #     resume_emb = embedder.encode(resume_text, convert_to_tensor=True)
# #     return util.cos_sim(jd_emb, resume_emb).item()

# # # -------------------------------
# # # Main Matching Function
# # # -------------------------------
# # def analyze_resume(jd_text, resume_text, jd_skills):
# #     # Skills match
# #     matched, missing = extract_skills(resume_text, jd_skills)
# #     skill_score = len(matched) / len(jd_skills) if jd_skills else 0

# #     # Semantic similarity
# #     sim_score = compute_similarity(jd_text, resume_text)

# #     # Weighted score (skills 60%, similarity 40%)
# #     final_score = round((0.6 * skill_score + 0.4 * sim_score) * 100, 2)

# #     return {
# #         "Match %": final_score,
# #         "Matched Skills": matched,
# #         "Missing Skills": missing
# #     }

# # # -------------------------------
# # # Example Usage
# # # -------------------------------
# # if __name__ == "__main__":
# #     # Input JD
# #     jd_text = """We are looking for a Data Scientist with 5+ years of experience.
# #     Skills required: Python, SQL, Machine Learning, Deep Learning, Cloud Computing.
# #     Education: Masters in Computer Science."""

# #     # Define JD skills (can also auto-extract using spacy NER or a skill dictionary)
# #     jd_skills = ["Python", "SQL", "Machine Learning", "Deep Learning", "Cloud Computing"]

# #     # Directory of resumes
# #     resume_dir = "resumes/"
# #     results = []

# #     for file in os.listdir(resume_dir):
# #         path = os.path.join(resume_dir, file)
# #         resume_text = extract_text(path)

# #         report = analyze_resume(jd_text, resume_text, jd_skills)
# #         report["Resume"] = file
# #         results.append(report)

# #     # Save results
# #     df = pd.DataFrame(results)
# #     print(df)
# #     df.to_csv("jd_resume_match_report.csv", index=False)
# import os
# import re
# import docx2txt
# import PyPDF2
# from sentence_transformers import SentenceTransformer, util
# import spacy
# import pandas as pd
# import logging

# # -------------------------------
# # Setup Logging
# # -------------------------------
# logging.basicConfig(
#     filename="jd_resume_match.log",
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )

# # -------------------------------
# # Load models
# # -------------------------------
# logging.info("Loading models...")
# embedder = SentenceTransformer('all-MiniLM-L6-v2')
# nlp = spacy.load("en_core_web_sm")
# logging.info("Models loaded successfully.")

# # -------------------------------
# # Helper functions
# # -------------------------------
# def extract_text(file_path):
#     """Extract text from PDF, DOCX or TXT."""
#     logging.info(f"Extracting text from: {file_path}")
#     text = ""
#     try:
#         if file_path.endswith(".pdf"):
#             with open(file_path, "rb") as f:
#                 reader = PyPDF2.PdfReader(f)
#                 for page_num, page in enumerate(reader.pages):
#                     page_text = page.extract_text()
#                     if page_text:
#                         text += page_text + "\n"
#             logging.info(f"Extracted {len(text)} characters from PDF {file_path}")

#         elif file_path.endswith(".docx"):
#             text = docx2txt.process(file_path)
#             logging.info(f"Extracted {len(text)} characters from DOCX {file_path}")

#         elif file_path.endswith(".txt"):
#             with open(file_path, "r", encoding="utf-8") as f:
#                 text = f.read()
#             logging.info(f"Extracted {len(text)} characters from TXT {file_path}")

#     except Exception as e:
#         logging.error(f"Error extracting text from {file_path}: {e}")
#     return text


# def clean_text(text):
#     """Basic text cleaning."""
#     return re.sub(r'[^a-zA-Z0-9 ]', ' ', text.lower())


# def extract_skills(text, jd_skills):
#     """Check which JD skills are present in resume."""
#     logging.info("Extracting skills...")
#     resume_tokens = set(clean_text(text).split())
#     matched = [skill for skill in jd_skills if skill.lower() in resume_tokens]
#     missing = [skill for skill in jd_skills if skill.lower() not in resume_tokens]
#     logging.info(f"Matched skills: {matched}")
#     logging.info(f"Missing skills: {missing}")
#     return matched, missing


# def compute_similarity(jd_text, resume_text):
#     """Semantic similarity using embeddings."""
#     logging.info("Computing semantic similarity...")
#     jd_emb = embedder.encode(jd_text, convert_to_tensor=True)
#     resume_emb = embedder.encode(resume_text, convert_to_tensor=True)
#     sim_score = util.cos_sim(jd_emb, resume_emb).item()
#     logging.info(f"Similarity Score: {sim_score:.4f}")
#     return sim_score


# # -------------------------------
# # Main Matching Function
# # -------------------------------
# def analyze_resume(jd_text, resume_text, jd_skills):
#     logging.info("Analyzing resume...")
    
#     # Skills match
#     matched, missing = extract_skills(resume_text, jd_skills)
#     skill_score = len(matched) / len(jd_skills) if jd_skills else 0
#     logging.info(f"Skill Score: {skill_score:.2f}")

#     # Semantic similarity
#     sim_score = compute_similarity(jd_text, resume_text)

#     # Weighted score (skills 60%, similarity 40%)
#     final_score = round((0.6 * skill_score + 0.4 * sim_score) * 100, 2)
#     logging.info(f"Final Match %: {final_score}")

#     return {
#         "Match %": final_score,
#         "Matched Skills": matched,
#         "Missing Skills": missing
#     }


# # -------------------------------
# # Example Usage
# # -------------------------------
# if __name__ == "__main__":
#     logging.info("Starting JD-Resume Matching...")

#     # Input JD
#     jd_text = """We are looking for a Data Scientist with 5+ years of experience.
#     Skills required: Python, SQL, Machine Learning, Deep Learning, Cloud Computing.
#     Education: Masters in Computer Science."""

#     # Define JD skills
#     jd_skills = ["Python", "SQL", "Machine Learning", "Deep Learning", "Cloud Computing"]

#     # Directory of resumes
#     resume_dir = "resumes/"
#     results = []

#     for file in os.listdir(resume_dir):
#         path = os.path.join(resume_dir, file)
#         logging.info(f"Processing resume: {file}")
#         resume_text = extract_text(path)

#         if not resume_text.strip():
#             logging.warning(f"No text extracted from {file}, skipping...")
#             continue

#         report = analyze_resume(jd_text, resume_text, jd_skills)
#         report["Resume"] = file
#         results.append(report)

#     # Save results
#     df = pd.DataFrame(results)
#     df.to_csv("jd_resume_match_report.csv", index=False)
#     logging.info("Matching complete. Results saved to jd_resume_match_report.csv")
import os
import re
import docx2txt
import PyPDF2
import pandas as pd
import streamlit as st
from sentence_transformers import SentenceTransformer, util
import spacy

# -------------------------------
# Load models
# -------------------------------
@st.cache_resource
def load_models():
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    nlp = spacy.load("en_core_web_sm")
    return embedder, nlp

embedder, nlp = load_models()

# -------------------------------
# Helper functions
# -------------------------------
def extract_text(file):
    """Extract text from PDF, DOCX or TXT (from uploaded file)."""
    text = ""
    if file.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    elif file.name.endswith(".docx"):
        text = docx2txt.process(file)

    elif file.name.endswith(".txt"):
        text = file.read().decode("utf-8")

    return text


def clean_text(text):
    """Basic text cleaning."""
    return re.sub(r'[^a-zA-Z0-9 ]', ' ', text.lower())


def extract_skills(text, jd_skills):
    """Check which JD skills are present in resume."""
    resume_tokens = set(clean_text(text).split())
    matched = [skill for skill in jd_skills if skill.lower() in resume_tokens]
    missing = [skill for skill in jd_skills if skill.lower() not in resume_tokens]
    return matched, missing


def compute_similarity(jd_text, resume_text):
    """Semantic similarity using embeddings."""
    jd_emb = embedder.encode(jd_text, convert_to_tensor=True)
    resume_emb = embedder.encode(resume_text, convert_to_tensor=True)
    return util.cos_sim(jd_emb, resume_emb).item()


def analyze_resume(jd_text, resume_text, jd_skills):
    # Skills match
    matched, missing = extract_skills(resume_text, jd_skills)
    skill_score = len(matched) / len(jd_skills) if jd_skills else 0

    # Semantic similarity
    sim_score = compute_similarity(jd_text, resume_text)

    # Weighted score (skills 60%, similarity 40%)
    final_score = round((0.6 * skill_score + 0.4 * sim_score) * 100, 2)

    return {
        "Match %": final_score,
        "Matched Skills": ", ".join(matched),
        "Missing Skills": ", ".join(missing)
    }

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="JD vs Resume Matcher", layout="wide")
st.title("📊 Job Description vs Resume Matcher")

# Two columns: JD input and Resume upload
col1, col2 = st.columns(2)

with col1:
    st.header("📌 Paste Job Description")
    jd_text = st.text_area("Enter JD here", height=300)

    jd_skills_text = st.text_input("Enter required skills (comma-separated)",
                                   value="Python, SQL, Machine Learning, Deep Learning, Cloud Computing")
    jd_skills = [s.strip() for s in jd_skills_text.split(",") if s.strip()]

with col2:
    st.header("📂 Upload Resumes")
    uploaded_files = st.file_uploader("Upload resumes (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"], accept_multiple_files=True)

# Process
if st.button("Analyze Resumes"):
    if jd_text.strip() and uploaded_files:
        results = []
        for file in uploaded_files:
            resume_text = extract_text(file)
            if not resume_text.strip():
                continue
            report = analyze_resume(jd_text, resume_text, jd_skills)
            report["Resume"] = file.name
            results.append(report)

        if results:
            df = pd.DataFrame(results)
            st.success("✅ Analysis Complete!")
            st.dataframe(df)

            # Option to download results
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download Report", data=csv, file_name="jd_resume_match_report.csv", mime="text/csv")
        else:
            st.warning("No valid text extracted from resumes.")
    else:
        st.error("Please paste JD and upload resumes before analysis.")
