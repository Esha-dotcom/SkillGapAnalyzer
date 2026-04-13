import re

# -------------------------------
# STEP 1: Extract Text (from txt files for simplicity)
# -------------------------------
def extract_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


# -------------------------------
# STEP 2: Clean Text
# -------------------------------
def clean_text(text):
    text = text.lower()  # convert to lowercase
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # remove special characters
    return text


# -------------------------------
# STEP 3: Skill List (Static)
# -------------------------------
SKILL_LIST = [
    "python", "java", "c++", "machine learning", "data science",
    "deep learning", "sql", "excel", "nlp", "tensorflow", "pandas"
]


# -------------------------------
# STEP 4: Match Skills
# -------------------------------
def match_skills(resume_text, job_desc_text, skill_list):
    matched = []
    missing = []

    combined_text = resume_text + " " + job_desc_text

    for skill in skill_list:
        if skill in combined_text:
            matched.append(skill)
        else:
            missing.append(skill)

    return matched, missing


# -------------------------------
# STEP 5: Calculate Match Percentage
# -------------------------------
def calculate_match_percentage(matched, total_skills):
    if total_skills == 0:
        return 0
    return (len(matched) / total_skills) * 100


# -------------------------------
# MAIN FUNCTION
# -------------------------------
def main():
    # File paths (change as needed)
    resume_file = "resume.txt"
    job_desc_file = "job_description.txt"

    # Extract text
    resume_text = extract_text(resume_file)
    job_desc_text = extract_text(job_desc_file)

    # Clean text
    resume_text = clean_text(resume_text)
    job_desc_text = clean_text(job_desc_text)

    # Match skills
    matched, missing = match_skills(resume_text, job_desc_text, SKILL_LIST)

    # Calculate percentage
    match_percentage = calculate_match_percentage(matched, len(SKILL_LIST))

    # Output
    print("\n===== RESULT =====")
    print(f"Matched Skills: {matched}")
    print(f"Missing Skills: {missing}")
    print(f"Match Percentage: {match_percentage:.2f}%")
    print("==================\n")


# Run the program
if __name__ == "__main__":
    main()