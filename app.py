import streamlit as st
import pandas as pd
import random
import re
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="SkillTwin AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #090d1a, #111827, #172554);
        color: white;
    }

    [data-testid="stSidebar"] {
        background: #080c18;
        border-right: 1px solid #26324d;
    }

    .hero {
        padding: 35px;
        border-radius: 25px;
        background: linear-gradient(135deg, #1e3a8a, #4f46e5, #7c3aed);
        box-shadow: 0 15px 45px rgba(0,0,0,0.35);
        margin-bottom: 25px;
    }

    .hero h1 {
        font-size: 48px;
        margin-bottom: 5px;
    }

    .hero p {
        font-size: 18px;
        color: #e0e7ff;
    }

    .card {
        padding: 22px;
        border-radius: 18px;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.10);
        margin-bottom: 18px;
    }

    .metric-card {
        padding: 22px;
        border-radius: 18px;
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.10);
        text-align: center;
    }

    .metric-number {
        font-size: 34px;
        font-weight: bold;
    }

    .metric-label {
        color: #a5b4fc;
        font-size: 14px;
    }

    .skill-good {
        color: #34d399;
        font-weight: bold;
    }

    .skill-mid {
        color: #fbbf24;
        font-weight: bold;
    }

    .skill-low {
        color: #fb7185;
        font-weight: bold;
    }

    .roadmap {
        padding: 20px;
        border-left: 4px solid #6366f1;
        background: rgba(99,102,241,0.10);
        border-radius: 12px;
        margin-bottom: 12px;
    }

    .question {
        padding: 22px;
        border-radius: 16px;
        background: rgba(79,70,229,0.12);
        border: 1px solid rgba(129,140,248,0.25);
        font-size: 18px;
    }

    .footer {
        text-align: center;
        color: #94a3b8;
        padding: 30px;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

if "profile" not in st.session_state:
    st.session_state.profile = {}

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "interview_score" not in st.session_state:
    st.session_state.interview_score = 0

if "question_index" not in st.session_state:
    st.session_state.question_index = 0


# =========================================================
# DATA
# =========================================================

CAREERS = {
    "AI/ML Engineer": {
        "Python": 85,
        "DSA": 70,
        "Machine Learning": 90,
        "Deep Learning": 85,
        "SQL": 65,
        "Communication": 65,
        "Projects": 80
    },
    "Data Scientist": {
        "Python": 85,
        "DSA": 60,
        "Machine Learning": 90,
        "Deep Learning": 70,
        "SQL": 85,
        "Communication": 75,
        "Projects": 75
    },
    "Python Developer": {
        "Python": 90,
        "DSA": 75,
        "Machine Learning": 45,
        "Deep Learning": 30,
        "SQL": 75,
        "Communication": 70,
        "Projects": 80
    },
    "Web Developer": {
        "Python": 65,
        "DSA": 65,
        "Machine Learning": 30,
        "Deep Learning": 20,
        "SQL": 70,
        "Communication": 75,
        "Projects": 85
    },
    "Software Engineer": {
        "Python": 75,
        "DSA": 90,
        "Machine Learning": 45,
        "Deep Learning": 25,
        "SQL": 70,
        "Communication": 75,
        "Projects": 85
    }
}

INTERVIEW_QUESTIONS = [
    {
        "q": "What is the difference between a list and a tuple in Python?",
        "keywords": ["list", "tuple", "mutable", "immutable"]
    },
    {
        "q": "What is supervised learning?",
        "keywords": ["labeled", "data", "prediction", "training"]
    },
    {
        "q": "What is overfitting in machine learning?",
        "keywords": ["training", "unseen", "generalization", "model"]
    },
    {
        "q": "What is the time complexity of binary search?",
        "keywords": ["log", "o(log", "sorted"]
    },
    {
        "q": "What is a primary key in SQL?",
        "keywords": ["unique", "identify", "record", "null"]
    }
]


# =========================================================
# FUNCTIONS
# =========================================================

def calculate_score(skills):
    weights = {
        "Python": 0.18,
        "DSA": 0.16,
        "Machine Learning": 0.18,
        "Deep Learning": 0.12,
        "SQL": 0.12,
        "Communication": 0.10,
        "Projects": 0.14
    }

    score = sum(skills[k] * weights[k] for k in weights)

    return round(score)


def career_match(skills):
    results = []

    for career, requirements in CAREERS.items():

        total = 0
        count = 0

        for skill in requirements:
            difference = abs(skills.get(skill, 0) - requirements[skill])
            match = max(0, 100 - difference)
            total += match
            count += 1

        percentage = round(total / count)

        results.append({
            "Career": career,
            "Match": percentage
        })

    return sorted(results, key=lambda x: x["Match"], reverse=True)


def get_level(score):
    if score >= 85:
        return "Elite 🚀"
    elif score >= 70:
        return "Job Ready 💼"
    elif score >= 55:
        return "Intermediate 📈"
    elif score >= 40:
        return "Beginner 🌱"
    return "Starter 🔰"


def get_gaps(skills):
    gaps = []

    for skill, value in skills.items():

        if value < 50:
            priority = "High"
        elif value < 70:
            priority = "Medium"
        else:
            priority = "Low"

        if value < 70:
            gaps.append({
                "Skill": skill,
                "Current": value,
                "Priority": priority
            })

    return gaps


def analyze_resume(text):
    text_lower = text.lower()

    skills = {
        "Python": ["python"],
        "Java": ["java"],
        "C++": ["c++", "cpp"],
        "Machine Learning": ["machine learning", "sklearn", "scikit"],
        "Deep Learning": ["deep learning", "tensorflow", "pytorch"],
        "SQL": ["sql", "mysql", "postgresql"],
        "Web Development": ["html", "css", "javascript", "flask", "django"],
        "Git": ["git", "github"],
        "Data Science": ["pandas", "numpy", "matplotlib"]
    }

    found = []

    for skill, words in skills.items():
        if any(word in text_lower for word in words):
            found.append(skill)

    words_count = len(re.findall(r"\b\w+\b", text))

    project_count = len(
        re.findall(
            r"\b(project|developed|built|created|implemented)\b",
            text_lower
        )
    )

    return found, words_count, project_count


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("## 🚀 SkillTwin AI")
st.sidebar.caption("Your Intelligent Career Twin")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "👤 Skill Profile",
        "🧠 AI Analysis",
        "🎯 Career Matcher",
        "🧩 Skill Gaps",
        "📅 Roadmap",
        "📄 Resume Analyzer",
        "🎤 Interview AI",
        "📈 Progress"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "SkillTwin AI helps students understand their skills, "
    "career readiness and learning priorities."
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.markdown("""
    <div class="hero">
        <h1>🚀 SkillTwin AI</h1>
        <p>Your AI-powered career readiness and skill-gap platform.</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.analysis:

        data = st.session_state.analysis
        score = data["score"]

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-number">{score}%</div>
                    <div class="metric-label">Career Readiness</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-number">{data["level"]}</div>
                    <div class="metric-label">Current Level</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-number">{len(data["gaps"])}</div>
                    <div class="metric-label">Skill Gaps</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c4:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-number">{data["career"][0]["Match"]}%</div>
                    <div class="metric-label">Top Career Match</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("### 📊 Your Skill Overview")

        chart = pd.DataFrame(
            {
                "Skill": list(data["skills"].keys()),
                "Score": list(data["skills"].values())
            }
        ).set_index("Skill")

        st.bar_chart(chart)

    else:

        st.markdown("""
        <div class="card">
            <h2>👋 Welcome to SkillTwin AI</h2>
            <p>
            Create your skill profile to unlock your career analysis,
            skill-gap detection, career matching and personalized roadmap.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.info("👉 Go to **Skill Profile** from the sidebar to begin.")


# =========================================================
# PROFILE
# =========================================================

elif page == "👤 Skill Profile":

    st.title("👤 Build Your Skill Profile")
    st.write("Tell SkillTwin AI about your current abilities.")

    name = st.text_input("Your Name", value=st.session_state.profile.get("name", ""))

    college = st.text_input(
        "College / University",
        value=st.session_state.profile.get("college", "")
    )

    branch = st.selectbox(
        "Branch",
        [
            "CSE",
            "CSE - AI/ML",
            "Information Science",
            "ECE",
            "EEE",
            "Mechanical",
            "Other"
        ]
    )

    year = st.selectbox(
        "Year",
        ["1st Year", "2nd Year", "3rd Year", "4th Year"]
    )

    st.markdown("### 🧠 Rate Your Skills")

    c1, c2 = st.columns(2)

    with c1:

        python_skill = st.slider("🐍 Python", 0, 100, 50)
        dsa_skill = st.slider("🧠 DSA", 0, 100, 50)
        ml_skill = st.slider("🤖 Machine Learning", 0, 100, 50)
        dl_skill = st.slider("🧬 Deep Learning", 0, 100, 30)

    with c2:

        sql_skill = st.slider("🗄️ SQL", 0, 100, 50)
        communication = st.slider("🎤 Communication", 0, 100, 50)
        projects = st.slider("💻 Project Experience", 0, 100, 40)

    target = st.selectbox(
        "🎯 Target Career",
        list(CAREERS.keys())
    )

    if st.button("🚀 Generate My Career Twin", use_container_width=True):

        skills = {
            "Python": python_skill,
            "DSA": dsa_skill,
            "Machine Learning": ml_skill,
            "Deep Learning": dl_skill,
            "SQL": sql_skill,
            "Communication": communication,
            "Projects": projects
        }

        score = calculate_score(skills)
        careers = career_match(skills)
        gaps = get_gaps(skills)

        st.session_state.profile = {
            "name": name,
            "college": college,
            "branch": branch,
            "year": year,
            "target": target
        }

        st.session_state.analysis = {
            "skills": skills,
            "score": score,
            "level": get_level(score),
            "career": careers,
            "gaps": gaps
        }

        st.success("🎉 Your AI Career Twin has been created!")

        st.rerun()


# =========================================================
# AI ANALYSIS
# =========================================================

elif page == "🧠 AI Analysis":

    st.title("🧠 AI Career Analysis")

    if not st.session_state.analysis:

        st.warning("Create your Skill Profile first.")

    else:

        data = st.session_state.analysis

        st.metric(
            "Overall Job Readiness",
            f"{data['score']}%"
        )

        st.progress(data["score"] / 100)

        st.markdown(
            f"""
            <div class="card">
                <h2>{data["level"]}</h2>
                <p>
                Based on your current skills, projects and technical
                abilities, SkillTwin AI estimates your current career readiness.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.subheader("🔍 AI Insights")

        skills = data["skills"]

        strongest = max(skills, key=skills.get)
        weakest = min(skills, key=skills.get)

        st.success(
            f"💪 Your strongest area is **{strongest} ({skills[strongest]}%)**."
        )

        st.warning(
            f"⚠️ Your biggest improvement area is **{weakest} ({skills[weakest]}%)**."
        )

        st.info(
            "🎯 Focus on your weakest two skills first. "
            "Improving them can significantly increase your job readiness."
        )


# =========================================================
# CAREER MATCHER
# =========================================================

elif page == "🎯 Career Matcher":

    st.title("🎯 AI Career Matcher")

    if not st.session_state.analysis:

        st.warning("Create your Skill Profile first.")

    else:

        careers = st.session_state.analysis["career"]

        df = pd.DataFrame(careers)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("🏆 Best Career Matches")

        for i, item in enumerate(careers[:3]):

            if i == 0:
                emoji = "🥇"
            elif i == 1:
                emoji = "🥈"
            else:
                emoji = "🥉"

            st.markdown(
                f"""
                <div class="card">
                    <h3>{emoji} {item['Career']}</h3>
                    <h2>{item['Match']}% Match</h2>
                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# SKILL GAPS
# =========================================================

elif page == "🧩 Skill Gaps":

    st.title("🧩 AI Skill Gap Detector")

    if not st.session_state.analysis:

        st.warning("Create your Skill Profile first.")

    else:

        gaps = st.session_state.analysis["gaps"]

        if not gaps:

            st.success("🎉 No major skill gaps detected!")

        else:

            for gap in gaps:

                if gap["Priority"] == "High":
                    icon = "🔴"
                elif gap["Priority"] == "Medium":
                    icon = "🟡"
                else:
                    icon = "🟢"

                st.markdown(
                    f"""
                    <div class="card">
                        <h3>{icon} {gap['Skill']}</h3>
                        <p>Current Level: {gap['Current']}%</p>
                        <p>Priority: <b>{gap['Priority']}</b></p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# =========================================================
# ROADMAP
# =========================================================

elif page == "📅 Roadmap":

    st.title("📅 Personalized 90-Day Roadmap")

    if not st.session_state.analysis:

        st.warning("Create your Skill Profile first.")

    else:

        gaps = st.session_state.analysis["gaps"]

        focus = [x["Skill"] for x in gaps[:3]]

        st.markdown("### 🎯 Your Focus Areas")

        if focus:
            st.write(", ".join(focus))
        else:
            st.write("Advanced learning and interview preparation.")

        roadmap = [
            (
                "Month 1",
                "Foundation",
                "Strengthen programming, DSA, SQL and core concepts."
            ),
            (
                "Month 2",
                "Project Building",
                "Build a real-world project and upload it to GitHub."
            ),
            (
                "Month 3",
                "Placement Preparation",
                "Practice interviews, aptitude, DSA and resume building."
            )
        ]

        for month, title, description in roadmap:

            st.markdown(
                f"""
                <div class="roadmap">
                    <h3>📌 {month} — {title}</h3>
                    <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.subheader("🔥 Weekly Strategy")

        weeks = [
            "Week 1: Revise fundamentals",
            "Week 2: Practice coding problems",
            "Week 3: Learn advanced concepts",
            "Week 4: Build mini project",
            "Week 5: Improve weak skill",
            "Week 6: Build major project",
            "Week 7: GitHub + resume",
            "Week 8: Interview preparation",
            "Week 9: DSA revision",
            "Week 10: Mock interviews",
            "Week 11: Aptitude + technical revision",
            "Week 12: Final placement preparation"
        ]

        for week in weeks:
            st.checkbox(week)


# =========================================================
# RESUME ANALYZER
# =========================================================

elif page == "📄 Resume Analyzer":

    st.title("📄 AI Resume Analyzer")

    st.write(
        "Paste your resume text below. SkillTwin AI will identify "
        "technical skills and basic project indicators."
    )

    resume = st.text_area(
        "Paste Resume",
        height=300,
        placeholder="Paste your resume content here..."
    )

    if st.button("🔍 Analyze Resume", use_container_width=True):

        if not resume.strip():

            st.error("Please enter your resume text.")

        else:

            found, word_count, project_count = analyze_resume(resume)

            st.subheader("📊 Resume Results")

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric("Skills Found", len(found))

            with c2:
                st.metric("Words", word_count)

            with c3:
                st.metric("Project Indicators", project_count)

            st.subheader("🛠️ Detected Skills")

            if found:

                for skill in found:
                    st.success(f"✅ {skill}")

            else:

                st.warning(
                    "No major technical skills detected. "
                    "Consider adding relevant skills to your resume."
                )

            st.subheader("💡 Resume Suggestions")

            suggestions = []

            if word_count < 150:
                suggestions.append(
                    "Add more details about projects and achievements."
                )

            if project_count < 2:
                suggestions.append(
                    "Add at least 2 strong project descriptions."
                )

            if "Git" not in found:
                suggestions.append(
                    "Mention Git/GitHub if you have used them."
                )

            if not suggestions:
                st.success("🔥 Your resume has a good basic structure.")

            else:

                for suggestion in suggestions:
                    st.info("💡 " + suggestion)


# =========================================================
# INTERVIEW AI
# =========================================================

elif page == "🎤 Interview AI":

    st.title("🎤 AI Interview Practice")

    st.write(
        "Practice technical interview questions and receive "
        "a keyword-based evaluation."
    )

    index = st.session_state.question_index

    question = INTERVIEW_QUESTIONS[index]

    st.markdown(
        f"""
        <div class="question">
            <b>Question {index + 1}</b><br><br>
            {question["q"]}
        </div>
        """,
        unsafe_allow_html=True
    )

    answer = st.text_area(
        "Your Answer",
        height=180
    )

    if st.button("🤖 Evaluate Answer", use_container_width=True):

        answer_lower = answer.lower()

        matched = [
            keyword
            for keyword in question["keywords"]
            if keyword.lower() in answer_lower
        ]

        score = round(
            (len(matched) / len(question["keywords"])) * 100
        )

        st.session_state.interview_score = score

        if score >= 75:

            st.success(
                f"🔥 Excellent answer! Score: {score}%"
            )

        elif score >= 50:

            st.warning(
                f"👍 Good attempt. Score: {score}%"
            )

        else:

            st.error(
                f"📚 Needs improvement. Score: {score}%"
            )

        st.write(
            f"Keywords covered: {len(matched)} / "
            f"{len(question['keywords'])}"
        )

    if st.button("➡️ Next Question"):

        st.session_state.question_index = (
            st.session_state.question_index + 1
        ) % len(INTERVIEW_QUESTIONS)

        st.rerun()


# =========================================================
# PROGRESS
# =========================================================

elif page == "📈 Progress":

    st.title("📈 Career Progress")

    if not st.session_state.analysis:

        st.warning("Create your Skill Profile first.")

    else:

        skills = st.session_state.analysis["skills"]

        st.subheader("Current Skills")

        df = pd.DataFrame(
            {
                "Skill": list(skills.keys()),
                "Score": list(skills.values())
            }
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            df.set_index("Skill")
        )

        st.subheader("🎤 Interview Performance")

        st.metric(
            "Latest Interview Score",
            f"{st.session_state.interview_score}%"
        )

        st.subheader("🏆 Achievements")

        achievements = []

        if st.session_state.analysis["score"] >= 70:
            achievements.append("🏆 Job Ready")

        if skills["Python"] >= 80:
            achievements.append("🐍 Python Pro")

        if skills["DSA"] >= 80:
            achievements.append("🧠 DSA Master")

        if skills["Machine Learning"] >= 80:
            achievements.append("🤖 ML Explorer")

        if skills["Projects"] >= 80:
            achievements.append("💻 Project Builder")

        if st.session_state.interview_score >= 80:
            achievements.append("🎤 Interview Champion")

        if achievements:

            for achievement in achievements:
                st.success(achievement)

        else:

            st.info(
                "Keep improving your skills to unlock achievements!"
            )

        # Download report

        profile = st.session_state.profile

        report = f"""
SKILLTWIN AI - CAREER REPORT
=============================

Name: {profile.get("name", "Student")}
College: {profile.get("college", "Not provided")}
Branch: {profile.get("branch", "Not provided")}
Year: {profile.get("year", "Not provided")}
Target Career: {profile.get("target", "Not provided")}

Career Readiness:
{st.session_state.analysis["score"]}%

Level:
{st.session_state.analysis["level"]}

SKILLS
------

"""

        for skill, value in skills.items():
            report += f"{skill}: {value}%\n"

        report += "\nCAREER MATCHES\n---------------\n"

        for career in st.session_state.analysis["career"]:
            report += (
                f"{career['Career']}: "
                f"{career['Match']}%\n"
            )

        report += "\nSKILL GAPS\n----------\n"

        for gap in st.session_state.analysis["gaps"]:
            report += (
                f"{gap['Skill']} - "
                f"{gap['Current']}% - "
                f"{gap['Priority']} priority\n"
            )

        report += f"""
        
Generated:
{datetime.now().strftime("%d-%m-%Y %H:%M")}
"""

        st.download_button(
            "📥 Download Career Report",
            report,
            file_name="SkillTwin_Career_Report.txt",
            mime="text/plain",
            use_container_width=True
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    🚀 SkillTwin AI • Intelligent Career Readiness Platform
    <br>
    Built with Python & Streamlit
</div>
""", unsafe_allow_html=True)