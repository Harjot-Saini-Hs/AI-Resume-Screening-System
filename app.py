from flask import Flask, render_template,request,redirect,send_file
import os
from resume_parser import extract_text
from skill_matcher import calculate_score
from database import collection
from suggestion_engine import generate_suggestions
from pdf_report import generate_pdf
app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():

    name = request.form["name"]
    email = request.form["email"]
    phone =request.form["phone"]

    job_description = request.form["job_description"]

    resume = request.files["resume"]

    filepath = os.path.join(app.config["UPLOAD_FOLDER"],resume.filename)

    resume.save(filepath)

    resume_text = extract_text(filepath)

    score,matched,missing = calculate_score(job_description,resume_text)

    suggestions = generate_suggestions(missing)



    


   
    recommendation =(
        "Excellent Match " if score >= 70 
        else "Good Match" if score >=40 
        else "Needs Improvement"
    )

    generate_pdf(
        name,
        email,
        phone,
        score,
        matched,
        missing,
        recommendation,
        suggestions
    )

    collection.insert_one({
        "name":name,
        "email":email,
        "phone":phone,
        "job_description":job_description,
        "resume_file":resume.filename,
        "score":score,
        "matched_skills":matched,
        "missing_skills":missing,
        "recommendation":recommendation
    })

    return render_template("result.html",
        score=score,
        matched=matched,
        missing=missing,
        recommendation=recommendation,
        suggestions=suggestions
    )
@app.route("/dashboard")
def dashboard():

    search = request.args.get("search")

    if search:
        results = list(collection.find({
            "$or":[
                {"name":{"$regex":search,"$options":"i"}},
                {"email":{"$regex":search,"$options":"i"}}
            ]
        }))
    else:
        results = list(collection.find())

    total_candidates =len(results)

    if total_candidates > 0:
        average_score = round(
            sum(result["score"] for result in results)/
            total_candidates,2
            )
    else: average_score = 0

    excellent = sum(1 for result in results if result["score"]>=70)
    good = sum(1 for result in results if 40 <= result["score"] <70)
    needs_improvement = sum(1 for result in results if result["score"]<40)

    return render_template("dashboard.html",
                        results=results,
                        total_candidates=total_candidates,
                        average_score=average_score,
                        excellent=excellent,
                        good=good,
                        needs_improvement=needs_improvement
                    )


from bson.objectid import ObjectId

@app.route("/delete/<id>")
def delete(id):
    collection.delete_one({"_id":ObjectId(id)})

    return redirect("/dashboard")

@app.route("/download")
def download():
    return send_file(
        "report.pdf",
        as_attachment = True
    )
    

if __name__ == "__main__":
    app.run(debug=True)