def match_skills(resume_skills, jd_skills):

    match = []
    missing = []

    for skill in jd_skills:
        if skill in resume_skills:
            match.append(skill)
        else:
            missing.append(skill)

    if len(jd_skills) == 0:
        score = 0
    else:
        score = int((len(match) / len(jd_skills)) * 100)

    return match, missing, score