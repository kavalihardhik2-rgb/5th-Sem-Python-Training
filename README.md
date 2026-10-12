# 5th Sem Python Training

This repository holds the work our team did during the 5th semester Python training sessions. It has two files: a Jupyter notebook with the training exercises, and `app.py`, the team project, a Streamlit web app called SkillTwin AI.

## Contents

- `python training.ipynb`: the Jupyter notebook we worked through during the training sessions.
- `app.py`: the team project, SkillTwin AI, a career readiness and skill-gap tool for students.

## SkillTwin AI

SkillTwin AI takes a student's self-rated skills and turns them into a career picture. A student fills in a profile with sliders for Python, DSA, machine learning, deep learning, SQL, communication and project experience. The app then:

- calculates an overall career readiness score and a readiness level (from Starter to Elite)
- compares the profile against five target careers (AI/ML Engineer, Data Scientist, Python Developer, Web Developer, Software Engineer) and ranks the matches
- lists skill gaps with a High, Medium or Low priority
- builds a 90-day roadmap around the weakest skills
- scans pasted resume text for technical skills, project mentions and missing basics such as Git
- runs a short interview practice mode that scores answers by keyword coverage
- tracks progress, shows achievements and offers a downloadable career report

The scoring is rule-based and meant for learning. It is a teaching project, not a real hiring assessment.

## Requirements

- Python 3.8 or newer
- streamlit
- pandas

## Running the app

Install the dependencies:

```bash
pip install streamlit pandas
```

Then start the app from the folder that contains `app.py`:

```bash
streamlit run app.py
```

Streamlit will print a local address (usually http://localhost:8501) and open it in your browser.

## How to use it

1. Open the Skill Profile page and enter your details.
2. Move the sliders to match your current level and choose a target career.
3. Click "Generate My Career Twin".
4. Explore the Dashboard, Career Matcher, Skill Gaps and Roadmap pages.
5. Paste a resume into the Resume Analyzer, or practice answers on the Interview AI page.

Most pages need a profile first. If a page shows a warning, go back to Skill Profile and generate your twin.

## Team

Built by our 5th semester team during the Python training sessions.
