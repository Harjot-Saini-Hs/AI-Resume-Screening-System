def generate_suggestions(missing):

    suggestions = []

    for skill in missing:

        suggestions.append(f"Learn {skill}")

    if "Git" in missing:
        suggestions.append("Upload your projects to GitHub")

    if "React" in missing:
        suggestions.append("Build a React project")

    if "SQL" in missing:
        suggestions.append("Practice SQL queries and database projects")

    if len(missing) == 0:
        suggestions.append("Excellent Resume! Keep your skills updated.")

    return suggestions