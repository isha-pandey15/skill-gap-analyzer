import streamlit as st
import re
from PyPDF2 import PdfReader
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
from dotenv import load_dotenv
load_dotenv()

from skill_analyzer import extract_skills, analyze_gap

st.set_page_config(page_title="AI Skill Gap Analyzer", page_icon="📊")

st.title("📊 AI Skill Gap Analyzer")
st.write("Upload Resume and compare with Job Description")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "txt"])

resume_text = ""

# ===============================
# READ FILE
# ===============================
if uploaded_file:

    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text

    elif uploaded_file.type == "text/plain":
        resume_text = uploaded_file.read().decode("utf-8")

    st.success("Resume uploaded successfully!")

job_desc = st.text_area("Paste Job Description", height=200)


# ===============================
# PDF REPORT GENERATOR
# ===============================
def generate_pdf(text):
    file_path = "report.pdf"
    c = canvas.Canvas(file_path)
    y = 800

    for line in text.split("\n"):
        c.drawString(40, y, line)
        y -= 20

    c.save()
    return file_path


# ===============================
# ANALYSIS BUTTON
# ===============================
if st.button("Analyze Skill Gap"):

    if resume_text == "" or job_desc.strip() == "":
        st.warning("Please upload resume and paste job description.")

    else:
        with st.spinner("Analyzing..."):

            skills = extract_skills(None, resume_text)
            result, score = analyze_gap(None, skills, job_desc)

        st.subheader("📋 Extracted Skills")
        st.write(skills)

        st.subheader("📊 Analysis Result")
        st.text(result)

        st.subheader("📈 Skill Match Score")
        st.progress(score)
        st.write(f"Match Score: {score}%")

        # ===============================
        # PIE CHART
        # ===============================
        labels = ["Matched", "Missing"]
        values = [score, 100 - score]

        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%')
        ax.set_title("Skill Match Visualization")

        st.pyplot(fig)

        # ===============================
        # DOWNLOAD REPORT
        # ===============================
        pdf_path = generate_pdf(result)

        with open(pdf_path, "rb") as file:
            st.download_button("📥 Download Report", file, "Skill_Report.pdf")