import re


SKILL_ALIASES = {
    "Python": [
        "python"
    ],

    "Django": [
        "django"
    ],

    "Flask": [
        "flask"
    ],

    "REST API": [
        "rest api",
        "rest apis",
        "restful api",
        "restful apis"
    ],

    "SQL": [
        "sql"
    ],

    "MySQL": [
        "mysql"
    ],

    "HTML": [
        "html",
        "html5"
    ],

    "CSS": [
        "css",
        "css3"
    ],

    "JavaScript": [
        "javascript",
        "java script"
    ],

    "Git": [
        "git"
    ],

    "GitHub": [
        "github",
        "git hub"
    ],

    "Power BI": [
        "power bi",
        "powerbi"
    ],

    "Docker": [
        "docker"
    ],

    "AWS": [
        "aws",
        "amazon web services"
    ],
}


def normalize_text(text):
    """
    Convert text into a clean searchable format.
    """

    text = text.lower()

    # REST API variations
    text = text.replace("rest apis", "rest api")
    text = text.replace("restful apis", "rest api")
    text = text.replace("restful api", "rest api")

    # HTML/CSS variations
    text = text.replace("html5", "html")
    text = text.replace("css3", "css")

    # GitHub variation
    text = text.replace("git hub", "github")

    # Power BI variation
    text = text.replace("powerbi", "power bi")

    # Remove unwanted special characters
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def skill_exists(skill, text):
    """
    Check whether a skill exists in the given text.
    """

    aliases = SKILL_ALIASES.get(skill, [skill.lower()])

    for alias in aliases:

        # Escape special characters
        pattern = r"\b" + re.escape(alias) + r"\b"

        if re.search(pattern, text):
            return True

    return False


def calculate_match_score(resume_text, job_description):

    # Normalize both texts
    resume_text = normalize_text(resume_text)
    job_description = normalize_text(job_description)

    matched_skills = []
    missing_skills = []

    # Check only skills mentioned in Job Description
    for skill in SKILL_ALIASES:

        if skill_exists(skill, job_description):

            if skill_exists(skill, resume_text):

                matched_skills.append(skill)

            else:

                missing_skills.append(skill)

    # Calculate ATS score
    total_skills = len(matched_skills) + len(missing_skills)

    if total_skills == 0:

        score = 0

    else:

        score = round(
            (len(matched_skills) / total_skills) * 100
        )

    return score, matched_skills, missing_skills