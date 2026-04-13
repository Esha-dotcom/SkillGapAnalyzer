# SkillGap AI – Career Assistant

## Overview

SkillGap AI is a Python-based application that analyzes resumes and job descriptions to identify skill gaps and provide career guidance. The system evaluates user skills against job requirements and generates actionable insights such as missing skills, match percentage, and recommendations.

---

## Features

* Resume and job description analysis
* Skill extraction and matching
* Match percentage calculation
* Identification of missing skills
* Learning roadmap suggestions
* Job recommendations
* Interactive interface using Streamlit

---

## Project Structure

```bash
SkillGapAI/
│
├── milestone1/
│   ├── app.py
│   ├── resume.txt
│   └── job_description.txt
│
├── milestone2/
│   ├── app.py
│   └── requirements.txt
│
├── milestone3/
│   ├── app.py
│   └── requirements.txt
│
├── milestone4/
│   ├── app.py
│   ├── requirements.txt
│   ├── skill_database.py
│   └── utils.py
│
└── README.md
```

---

## Tech Stack

* Programming Language: Python
* Framework: Streamlit
* Libraries: Pandas, Regular Expressions, NLP-based enhancements

---

## Installation and Setup

### Clone the repository

```bash
git clone https://github.com/Esha-dotcom/SkillGapAI.git
cd SkillGapAI
```

### Install dependencies

```bash
cd milestone4
pip install -r requirements.txt
```

### Run the application

```bash
streamlit run app.py
```

---

## How It Works

1. The user provides a resume and a job description
2. The system extracts and preprocesses the text
3. Relevant skills are identified and matched
4. A match percentage is calculated
5. Missing skills and recommendations are generated

---

## Milestones

* Milestone 1: Basic text extraction and static skill matching
* Milestone 2: Improved preprocessing and text handling
* Milestone 3: Modular structure and enhanced logic
* Milestone 4: Skill database integration and advanced recommendations

---

## Future Scope

* Integration of advanced NLP models
* Real-time job data integration
* Resume improvement suggestions
* Deployment on cloud platforms

---

## Author

Esha K P

---

## Conclusion

SkillGap AI provides a structured approach to identifying and bridging skill gaps, enabling users to align their profiles with industry requirements effectively.

---

