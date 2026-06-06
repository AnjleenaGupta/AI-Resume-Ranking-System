import os
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
import pdfplumber
from groq import Groq

# Load environment variables
load_dotenv()

# ---------------- GROQ CLIENT ----------------
client = Groq(
    api_key=os.getenv(
        "GROQ_API_KEY"
    )
)



# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Resume Ranking System",
    page_icon="📄",
    layout="wide"
)

# ---------------- METRICS ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "AI Model",
        "Llama 3.3"
    )

with col2:
    st.metric(
        "Resume Ranking",
        "Enabled ✅"
    )

with col3:
    st.metric(
        "ATS Analysis",
        "Ready 🚀"
    )

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

h1, h2, h3 {
    color: #00E5FF;
}

section[data-testid="stSidebar"] {
    background-color: #161B22;
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 3em;
    font-size: 16px;
    font-weight: bold;
}

[data-testid="metric-container"] {
    background-color: #1E293B;
    border: 1px solid #334155;
    padding: 15px;
    border-radius: 15px;
}

.stProgress > div > div > div > div {
    background-color: #00E676;
}

.stSuccess {
    border-radius: 12px;
}

.resume-card {
    background-color: #1E293B;
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 20px;
    border: 1px solid #334155;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("""
<h1 style='text-align:center;'>
📄 AI Resume Ranking System
</h1>
""", unsafe_allow_html=True)

st.write(
    "Upload multiple resumes and rank candidates "
    "based on Job Description matching."
)

# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.header("🚀 About Project")

    st.info("""
    Features:
    ✅ Multiple Resume Upload
    ✅ Resume Ranking
    ✅ ATS Score
    ✅ Job Description Matching
    ✅ AI Feedback
    ✅ CSV Download Report
    """)

# ---------------- PDF TEXT EXTRACTION ----------------
def extract_resume_text(file):

    text = ""

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted

    return text

# ---------------- FILE UPLOAD ----------------
uploaded_files = st.file_uploader(
    "Upload Resumes (PDF)",
    type="pdf",
    accept_multiple_files=True
)

# ---------------- JOB DESCRIPTION ----------------
job_description = st.text_area(
    "Paste Job Description Here"
)

# ---------------- ANALYZE BUTTON ----------------
if st.button("Analyze Resumes"):

    resume_scores = []

    if not uploaded_files:

        st.warning(
            "Please upload resumes first"
        )

    elif not job_description:

        st.warning(
            "Please enter job description"
        )

    else:

        st.success(
            f"{len(uploaded_files)} resumes uploaded successfully!"
        )

        # ---------------- SKILLS ----------------
        skills = [
            "Python",
            "SQL",
            "Machine Learning",
            "Deep Learning",
            "Artificial Intelligence",
            "C++",
            "Java",
            "DSA",
            "NLP",
            "Pandas",
            "NumPy",
            "TensorFlow",
            "DBMS",
            "OOPs",
            "Git"
        ]

        # ---------------- SKILL ALIASES ----------------
        skill_aliases = {

            "Python": [
                "python"
            ],

            "SQL": [
                "sql"
            ],

            "Machine Learning": [
                "machine learning",
                "ml"
            ],

            "Deep Learning": [
                "deep learning"
            ],

            "Artificial Intelligence": [
                "artificial intelligence",
                "ai"
            ],

            "C++": [
                "c++",
                "c plus plus"
            ],

            "Java": [
                "java",
                "core java"
            ],

            "DSA": [
                "dsa",
                "data structures",
                "algorithms",
                "data structures & algorithms"
            ],

            "NLP": [
                "nlp",
                "natural language processing"
            ],

            "Pandas": [
                "pandas"
            ],

            "NumPy": [
                "numpy"
            ],

            "TensorFlow": [
                "tensorflow"
            ],

            "DBMS": [
                "dbms",
                "database management system",
                "database"
            ],

            "OOPs": [
                "oops",
                "object oriented programming"
            ],

            "Git": [
                "git",
                "github"
            ]
        }

        # ---------------- WEIGHTED SCORING ----------------
        skill_weights = {
            "Python": 20,
            "Machine Learning": 20,
            "SQL": 15,
            "DBMS": 10,
            "Java": 15,
            "C++": 15,
            "Git": 5,
            "DSA": 10,
            "Deep Learning": 15,
            "NLP": 10,
            "TensorFlow": 10,
            "Pandas": 5,
            "NumPy": 5,
            "OOPs": 10
        }

        st.subheader(
            "📊 Resume Analysis"
        )

        # ---------------- ANALYZE EACH RESUME ----------------
        for file in uploaded_files:

            resume_text = extract_resume_text(
                file
            )

            detected_skills = []

            # Detect skills
            for skill, keywords in (
                skill_aliases.items()
            ):

                for keyword in keywords:

                    if (
                        keyword
                        in resume_text.lower()
                    ):

                        detected_skills.append(
                            skill
                        )

                        break

            matched_skills = []

            earned_score = 0
            total_score = 0

            # JD matching
            for skill in skills:

                jd_match = False

                for keyword in (
                    skill_aliases.get(
                        skill,
                        [skill.lower()]
                    )
                ):

                    if (
                        keyword
                        in job_description.lower()
                    ):

                        jd_match = True
                        break

                if jd_match:

                    total_score += (
                        skill_weights.get(
                            skill,
                            5
                        )
                    )

                    if (
                        skill
                        in detected_skills
                    ):

                        matched_skills.append(
                            skill
                        )

                        earned_score += (
                            skill_weights.get(
                                skill,
                                5
                            )
                        )

            # Final score
            if total_score > 0:

                score = int(
                    (
                        earned_score
                        / total_score
                    ) * 100
                )

            else:
                score = 0

            # Save result
            resume_scores.append(
                {
                    "name": file.name,
                    "score": score,
                    "skills": detected_skills,
                    "matched": matched_skills
                }
            )

        # ---------------- SORT RANK ----------------
        resume_scores.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        # ---------------- CSV DOWNLOAD ----------------
        report_data = []

        for index, resume in enumerate(
            resume_scores
        ):

            report_data.append(
                {
                    "Rank": index + 1,
                    "Candidate Name": resume["name"],
                    "Match Score": f"{resume['score']}%",
                    "Detected Skills": ", ".join(
                        resume["skills"]
                    ),
                    "Matched Skills": ", ".join(
                        resume["matched"]
                    )
                }
            )

        df = pd.DataFrame(
            report_data
        )

        csv = df.to_csv(
            index=False
        )

        st.download_button(
            label="📥 Download Ranking Report",
            data=csv,
            file_name="resume_ranking_report.csv",
            mime="text/csv"
        )

        st.subheader(
            "🏆 Candidate Ranking"
        )

        # ---------------- DISPLAY RESULTS ----------------
        for index, resume in enumerate(
            resume_scores
        ):

            st.divider()

            rank = index + 1

            if rank == 1:
                medal = "🥇"
            elif rank == 2:
                medal = "🥈"
            elif rank == 3:
                medal = "🥉"
            else:
                medal = "📄"

            st.markdown(
                '<div class="resume-card">',
                unsafe_allow_html=True
            )

            st.subheader(
                f"{medal} Rank #{rank} - {resume['name']}"
            )

            score = resume["score"]

            if score >= 70:

                st.success(
                    f"🔥 Excellent Match: {score}%"
                )

            elif score >= 40:

                st.warning(
                    f"⚡ Moderate Match: {score}%"
                )

            else:

                st.error(
                    f"❌ Low Match: {score}%"
                )

            st.progress(
                score / 100
            )

            if rank == 1:

                st.success(
                    "🏆 Top Candidate"
                )

            # Skills
            st.write(
                "### ✅ Detected Skills"
            )

            if resume["skills"]:

                for skill in (
                    resume["skills"]
                ):

                    st.write(
                        f"✔ {skill}"
                    )

            else:

                st.warning(
                    "No skills detected"
                )

            st.write(
                "### 🎯 Matched Skills"
            )

            if resume["matched"]:

                for skill in (
                    resume["matched"]
                ):

                    st.success(
                        skill
                    )

            else:

                st.error(
                    "No matching skills found"
                )

            # ---------------- AI FEEDBACK ----------------
            st.subheader(
                "🤖 AI Resume Feedback"
            )

            feedback_prompt = f"""
You are an expert resume reviewer.

Analyze this resume candidate.

Candidate Name:
{resume["name"]}

Detected Skills:
{resume["skills"]}

Matched Skills:
{resume["matched"]}

Match Score:
{resume["score"]}%

Give:
1. Strengths
2. Missing Skills
3. Resume Improvements
4. Final Hiring Recommendation

Keep response short and professional.
"""

            try:

                with st.spinner(
                    f"Generating AI feedback for {resume['name']}..."
                ):

                    response = (
                        client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[
                                {
                                    "role": "user",
                                    "content": feedback_prompt
                                }
                            ]
                        )
                    )

                    ai_feedback = (
                        response.choices[0]
                        .message.content
                    )

                    st.write(
                        ai_feedback
                    )

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

