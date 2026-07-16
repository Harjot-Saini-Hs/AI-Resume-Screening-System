from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

skills_weights = {
    "python":5,
    "html":2,
    "css":2,
    "javascript":3,
    "flask":4,
    "mongodb":4,
    "react":4,
    "node.js":4,
    "sql":3,
    "git":2,
    
}

def calculate_score(job_description, resume_text):

    matched = []
    missing =[]

    
    resume_lower = resume_text.lower()

    job_lower = job_description.lower()

    total_weight = 0
    matched_weight = 0

    for skill,weight in skills_weights.items():

        if skill in job_lower:
            total_weight += weight

            if skill in resume_lower:
                matched.append(skill.title())
                matched_weight += weight
            else:
                missing.append(skill.title())

    if total_weight == 0:
        score = 0
    else:
        score = round((matched_weight/total_weight)*100,2)

    return score, matched, missing