SKILLS_DB = [
"python","sql","machine learning","deep learning","statistics",
"excel","power bi","tableau","data analysis","communication",
"html","css","javascript","react"
]

def extract_skills(text):

    skills_found = []

    text = text.lower()

    for skill in SKILLS_DB:
        if skill in text:
            skills_found.append(skill)

    return list(set(skills_found))