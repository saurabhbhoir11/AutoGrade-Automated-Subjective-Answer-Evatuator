from flask import *
import scoreGenerator
import answerSeparator
import math
import textExtractor
import keywordsExtractor
import pandas as pd
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Load the models once at the start
textExtractor = textExtractor.textExtractor()
separator = answerSeparator.answerSeparator()
score = scoreGenerator.scoreGenerator()
keywordsExtractor = keywordsExtractor.keyWords()

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/upload', methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        name = request.form.get('name')
        department = request.form.get('department')
        year = request.form.get('year')
        rollno = request.form.get('rollno')
        division = request.form.get('division')
        subject = request.form.get('subject')
        student_answers = request.files['student_answers']
        model_answers = request.files['model_answers']
        student_answers.save(os.path.join(app.config['UPLOAD_FOLDER'], 'student_answers.pdf'))
        model_answers.save(os.path.join(app.config['UPLOAD_FOLDER'], 'model_answers.pdf'))
        return redirect(url_for('evaluate', name=name, department=department, year=year, rollno=rollno, division=division, subject=subject))

@app.route('/evaluate/<name>/<department>/<year>/<rollno>/<division>/<subject>', methods=['GET', 'POST'])
def evaluate(name, department, year, rollno, division, subject):
    if request.method == 'POST':

        # Use the loaded models
        student_answers_text = textExtractor.extractText(os.path.join(app.config['UPLOAD_FOLDER'], 'student_answers.pdf'))
        model_answers_text = textExtractor.extractText(os.path.join(app.config['UPLOAD_FOLDER'], 'model_answers.pdf'))

        student_answers = separator.parse_questions(student_answers_text)
        model_answers = separator.parse_answers(model_answers_text)

        solution = score.generateScore(student_answers, model_answers)

        total = 0

        for key in solution:
            if key in ["2A", "2B", "3A", "3B"]:
                solution[key] = math.ceil(solution[key] * 10)
            else:
                solution[key] = math.ceil(solution[key] * 5)
            total += solution[key]

        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], 'student_answers.pdf'))
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], 'model_answers.pdf'))

        return redirect(url_for('results', name=name, department=department, year=year, rollno=rollno, division=division, subject=subject, total=total))

    return render_template('evaluate.html')

@app.route('/results/<name>/<department>/<year>/<rollno>/<division>/<subject>/<total>')
def results(name, department, year, rollno, division, subject, total):
    return render_template('result.html', name=name, department=department, year=year, rollno=rollno, division=division, subject=subject, total=total)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
