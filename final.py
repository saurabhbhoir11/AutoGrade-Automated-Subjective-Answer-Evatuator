from flask import *
import scoreGenerator
import answerSeparator
import math
import textExtractor
import keywordsExtractor
import os

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads/"
app.secret_key = "secret"

# Load the models once at the start
textExtractor = textExtractor.textExtractor()
separator = answerSeparator.answerSeparator()
score = scoreGenerator.scoreGenerator()
keywordsExtractor = keywordsExtractor.keyWords()
temp = {}


@app.route("/")
def index():
    return render_template("form.html")


@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == "POST":
        name = request.form.get("name")
        session["name"] = name
        department = request.form.get("department")
        session["department"] = department
        year = request.form.get("year")
        session["year"] = year
        rollno = request.form.get("rollno")
        session["rollno"] = rollno
        division = request.form.get("division")
        session["division"] = division
        subject = request.form.get("subject")
        session["subject"] = subject
        student_answers = request.files["student_answers"]
        fname = student_answers.filename
        student_answers.save(
            os.path.join(app.config["UPLOAD_FOLDER"], fname)
        )
        text, count = textExtractor.extractText(
            os.path.join(app.config["UPLOAD_FOLDER"], fname)
        )
        session["count"] = count
        temp['rawText'] = text
        return redirect(url_for("display_original"))


@app.route("/display_original", methods=["GET", "POST"])
def display_original():
    count = session['count']
    images = []
    for i in range(count):
        images.append(f"displayImages/OriginalPage_{i}.png")
    return render_template("displayImages.html", images=images)


@app.route("/display_thresholded", methods=["GET", "POST"])
def display_thresholded():
    count = session['count']
    images = []
    for i in range(count):
        images.append(f"displayImages/DenoisedPage_{i}.png")
    return render_template("displayThresholded.html", images=images)


@app.route("/display_raw_text", methods=["GET", "POST"])
def display_raw_text():
    text = temp['rawText']
    return render_template("displayRawText.html", text=text)


@app.route("/display_separated_answers", methods=["GET", "POST"])
def display_separated_answers():
    student_answers = separator.parse_questions(temp['rawText'])
    with open("answers.txt", "r", encoding="utf-8") as file:
        model_answers_text = file.read()
    model_answers = separator.parse_answers(model_answers_text)
    temp['student_answers'] = student_answers
    temp['model_answers'] = model_answers
    display = []
    for key in student_answers:
        display.append((key, student_answers[key].split(". ")))
    return render_template("displaySeparatedAnswers.html", display=display)


@app.route("/display_raw_score", methods=["GET", "POST"])
def display_raw_score():
    solution, display = score.generateScore(temp['student_answers'], temp['model_answers'])
    temp['solution'] = solution
    return render_template("displayEmbeddings.html", display=display)


@app.route("/results")
def results():
    total = 0
    solution = temp['solution']
    scores = []
    for key in solution:
        if key in ["2A", "2B", "3A", "3B"]:
            solution[key] = math.ceil(solution[key] * 10)
        else:
            solution[key] = math.ceil(solution[key] * 5)
        total += solution[key]
        scores.append((key, solution[key]))
    print(scores)
    temp.clear()

    return render_template(
        "result.html",
        name=session["name"],
        department=session["department"],
        year=session["year"],
        rollno=session["rollno"],
        division=session["division"],
        subject=session["subject"],
        total=total,
        scores=scores,
    )


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
