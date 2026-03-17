def generate_roadmap(missing_skills):

    roadmap = []

    for skill in missing_skills:

        if skill == "statistics":
            roadmap.append("Learn Statistics Fundamentals")

        elif skill == "machine learning":
            roadmap.append("Learn Machine Learning Algorithms")

        elif skill == "deep learning":
            roadmap.append("Study Neural Networks and Deep Learning")

        elif skill == "excel":
            roadmap.append("Master Excel for Data Analysis")

        else:
            roadmap.append(f"Learn {skill.title()}")

    return roadmap