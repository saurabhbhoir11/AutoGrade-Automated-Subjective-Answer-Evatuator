from flask import *
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, Email
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from pdf2image import convert_from_path
import os
<<<<<<< HEAD
import cv2
import re
=======
>>>>>>> c7999fc1637e003214e4a7fa1fd180ca58aac016
from flask_pymongo import PyMongo
from google.cloud import vision, storage
import circleRemoval
import lineRemoval

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)
app.config['SECRET_KEY'] = 'your_secret_key'

app.config["UPLOAD_FOLDER"] = "uploads"
app.config["ALLOWED_EXTENSIONS"] = {"pdf"}

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "creds.json"

app.config["MONGO_URI_TEACHERS"] = "mongodb://localhost:27017/myDatabaseTeachers"
app.config["MONGO_URI_STUDENTS"] = "mongodb://localhost:27017/myDatabaseStudents"

mongo_teachers = PyMongo(app, uri=app.config["MONGO_URI_TEACHERS"])
mongo_students = PyMongo(app, uri=app.config["MONGO_URI_STUDENTS"])

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    query = TextAreaField('Query', validators=[DataRequired()])
    submit = SubmitField('Submit')

class TeacherUploadForm(FlaskForm):
    subject = StringField("Subject", validators=[DataRequired()])
    file = FileField("Answer Bank", validators=[DataRequired()])
    submit = SubmitField("Upload")

class StudentUploadForm(FlaskForm):
    subject = SelectField("Subject", validators=[DataRequired()])
    file = FileField("Answer PDF", validators=[DataRequired()])
    submit = SubmitField("Upload")

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )

def save_to_mongo(text, filename):
    # Access the MongoDB collection (create it if it doesn't exist)
    db = mongo.db
    collection = db["Autograde"]

    # Create a document to insert into the collection
    document = {"filename": filename, "text": text}

    # Insert the document into the collection
    collection.insert_one(document)

    return jsonify({"message": "Data saved to MongoDB successfully"})

def delete_existing_results(gcs_destination_uri):
    storage_client = storage.Client()
    match = re.match(r"gs://([^/]+)/(.+)", gcs_destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)
    bucket = storage_client.get_bucket(bucket_name)

    # List and delete objects with the given prefix
    for blob in list(bucket.list_blobs(prefix=prefix)):
        blob.delete()

# noinspection PyTypeChecker
def async_detect_document(filepath, gcs_destination_uri):
    text = ""
    """OCR with PDF/TIFF as source files on GCS"""
    import json
    import re
    import os

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "creds.json"

    from google.cloud import vision
    from google.cloud import storage

    # Set your GCS bucket and object name for the uploaded file
    gcs_bucket_name = "autograde_papers"
    gcs_object_name = "Doc1.pdf"  # Change to the desired object name

    # Initialize a GCS client
    storage_client = storage.Client()

    # Upload the local file to GCS
    bucket = storage_client.get_bucket(gcs_bucket_name)
    blob = bucket.blob(gcs_object_name)
    blob.upload_from_filename(filepath)

    # Supported mime_types are: 'application/pdf' and 'image/tiff'
    mime_type = "application/pdf"

    # How many pages should be grouped into each json output file.
    batch_size = 50

    client = vision.ImageAnnotatorClient()

    feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)

    gcs_source_uri = f"gs://{gcs_bucket_name}/{gcs_object_name}"
    gcs_source = vision.GcsSource(uri=gcs_source_uri)
    input_config = vision.InputConfig(gcs_source=gcs_source, mime_type=mime_type)

    gcs_destination = vision.GcsDestination(uri=gcs_destination_uri)
    output_config = vision.OutputConfig(
        gcs_destination=gcs_destination, batch_size=batch_size
    )

    async_request = vision.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config, output_config=output_config
    )

    operation = client.async_batch_annotate_files(requests=[async_request])

    print("Waiting for the operation to finish.")
    operation.result(timeout=420)

    # Once the request has completed and the output has been
    # written to GCS, we can list all the output files.
    match = re.match(r"gs://([^/]+)/(.+)", gcs_destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)

    bucket = storage_client.get_bucket(bucket_name)

    # List objects with the given prefix, filtering out folders.
    blob_list = [
        blob
        for blob in list(bucket.list_blobs(prefix=prefix))
        if not blob.name.endswith("/")
    ]
    print("Output files:")
    for blob in blob_list:
        print(blob.name)

    # Process text from all output files
    for output in blob_list:
        json_string = output.download_as_text()
        response = json.loads(json_string)

        # Extract text line by line from each page
        for page_response in response["responses"]:
            annotation = page_response.get("fullTextAnnotation", {})
            for page in annotation.get("pages", []):
                for block in page.get("blocks", []):
                    for paragraph in block.get("paragraphs", []):
                        for word_info in paragraph.get("words", []):
                            word = "".join([symbol["text"] for symbol in word_info.get("symbols", [])])
                            text += word + " "
                        text = text.rstrip()  # Remove trailing space
                        text += "\n"  # Add a newline between paragraphs

    return text

def textByGoogle(filepath, filename):
    gcs_destination_uri = "gs://autograde_papers/results"
    delete_existing_results(gcs_destination_uri)

    # Call the function to extract text from the PDF and store it
    async_detect_document(filepath, gcs_destination_uri)

    # Optionally, you can fetch text from MongoDB here if you've stored it there.
    text = async_detect_document(filepath, gcs_destination_uri)
    save_to_mongo(text, filename)
    return text

def clear_upload_folder():
    folder_path = app.config["UPLOAD_FOLDER"]
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):


            import shutil
            shutil.rmtree(file_path)

def generateImagesFromPDF(filepath):
    images = convert_from_path(filepath)
    num = 0
    page_images = []
    for i, image in enumerate(images):
        img_path = os.path.join(app.config["UPLOAD_FOLDER"], f"page_{i}.png")
        image.save(img_path)
        page_images.append(img_path)
        num = num + 1
    return page_images, num

def prerocessImage(image):
    image = circleRemoval.page_hole_removal(image)
    for _ in range(10):
        image = lineRemoval.lines_removal(image)
    return image

<<<<<<< HEAD
def textByTesseract(num):
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    text = ""
    for i in range(0, num):
        filename = "page_" + str(i) + ".png"
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        image = cv2.imread(filepath)
        print(filepath)
        image = prerocessImage(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        custom_config = r"--oem 3 --psm 6 -l eng"
        extracted_text = pytesseract.image_to_string(image, config=custom_config)
        text = text + extracted_text
    return text
=======


# def textByGoogleImg(num):
>>>>>>> c7999fc1637e003214e4a7fa1fd180ca58aac016

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        # Process the form data (for now, just display a flash message)
        flash('Query submitted successfully!, We will get in touch with you soon', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html', form=form)

@app.route("/dashboard")
def dashboard():
    if "username" not in session or "user_type" not in session:
        return redirect(url_for("home"))

    username = session["username"]
    user_type = session["user_type"]

    # Render the appropriate dashboard template based on user type
    if user_type == "teacher" or user_type == "student":
        # Assuming you have a dashboard template for teachers and students
        return render_template("dashboard.html", username=username)
    else:
        # Handle unknown user types or errors
        return redirect(url_for("home"))

# Teacher Upload Page Route
@app.route("/upload_teacher", methods=["GET", "POST"])
def upload_teacher():
    if "username" not in session:
        return redirect(url_for("home"))

    username = session["username"]
    user_type = session["user_type"]

    form = TeacherUploadForm(request.form)  # Assuming you have a form class for teacher upload

    if request.method == "POST" and form.validate_on_submit():
        file = request.files["file"]
        subject = form.subject.data  # Get the subject entered by the teacher

        if file and allowed_file(file.filename):
            clear_upload_folder()
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            # Save the answer bank data to the teacher's collection
            mongo_teachers.db.AnswerBank.insert_one({
                "username": username,
                "filename": filename,
                "subject": subject,
                "file_path": filepath
                # Add other fields as needed
            })

<<<<<<< HEAD
            flash("Answer bank successfully uploaded.", "success")
=======
            if selected_option == "pytesseract":
                page_images, num = generateImagesFromPDF(filepath)
                pass
>>>>>>> c7999fc1637e003214e4a7fa1fd180ca58aac016

            return redirect(url_for("upload_teacher"))  # Redirect to the teacher upload page

    return render_template("upload_teacher.html", form=form)

# Student Upload Page Route
@app.route("/upload_student", methods=["GET", "POST"])
def upload_student():
    if "username" not in session:
        return redirect(url_for("home"))

    username = session["username"]
    user_type = session["user_type"]

    # Fetch subjects for the student to choose from
    subjects = mongo_teachers.db.AnswerBank.distinct("subject")

    form = StudentUploadForm(request.form)  # Assuming you have a form class for student upload

    # Update the subject choices in the form
    form.subject.choices = [(subject, subject) for subject in subjects]

    if request.method == "POST" and form.validate_on_submit():
        file = request.files["file"]
        subject = form.subject.data

        if file and allowed_file(file.filename):
            clear_upload_folder()
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            # Save the student's answer PDF along with the subject
            mongo_students.db.StudentAnswers.insert_one({
                "username": username,
                "filename": filename,
                "subject": subject,
                "file_path": filepath
                # Add other fields as needed
            })

            flash("Answer PDF successfully uploaded.", "success")

            return redirect(url_for("upload_student"))  # Redirect to the student upload page

    return redirect(url_for("upload_student", form=form))

@app.route("/signup_teacher", methods=["GET", "POST"])
def signup_teacher():
    if request.method == "POST":
        # Get form data
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if the username is already taken
        if mongo_teachers.db.Teachers.find_one({"username": username}):
            flash("Username already taken. Please choose another.", "danger")
            return redirect(url_for("signup_teacher"))
        
        if not is_strong_password(password):
            flash("Password is weak. It should contain at least 8 characters, including uppercase, lowercase, and digits.", "danger")
            return redirect(url_for("signup_teacher"))

        # Hash the password using bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        # Insert new teacher into the database
        mongo_teachers.db.Teachers.insert_one({"username": username, "password": hashed_password, "email": email})
        
        # Set session variable for authentication
        session["username"] = username
        return redirect(url_for("login_teacher"))

    return render_template("signup_teacher.html")

@app.route("/signup_student", methods=["GET", "POST"])
def signup_student():
    if request.method == "POST":
        # Get form data
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if the username is already taken
        if mongo_students.db.Students.find_one({"username": username}):
            flash("Username already taken. Please choose another.", "danger")
            return redirect(url_for("signup_student"))
        
        if not is_strong_password(password):
            flash("Password is weak. It should contain at least 8 characters, including uppercase, lowercase, and digits.", "danger")
            return redirect(url_for("signup_student"))

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        # Insert new student into the database
        mongo_students.db.Students.insert_one({"username": username, "password": hashed_password, email: email})
        
        # Set session variable for authentication
        session["username"] = username
        return redirect(url_for("login_student"))

    return render_template

("signup_student.html")

@app.route("/login_teacher", methods=["GET", "POST"])
def login_teacher():
    if request.method == "POST":
        # Get form data
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if the username exists in the database
        teacher = mongo_teachers.db.Teachers.find_one({"username": username})

        if teacher:
            # Check if the password is correct using bcrypt
            if bcrypt.check_password_hash(teacher["password"], password):
                # Set session variable for authentication
                session["username"] = username
                session["user_type"] = "teacher"
                return redirect(url_for("dashboard"))
            else:
                flash("Incorrect password", "danger")
                return redirect(url_for("login_teacher"))
        else:
            flash("Username does not exist", "danger")
            return redirect(url_for("login_teacher"))

    return render_template("login_teacher.html")

@app.route("/login_student", methods=["GET", "POST"])
def login_student():
    if request.method == "POST":
        # Get form data
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if the username exists in the database
        student = mongo_students.db.Students.find_one({"username": username})

        if student:
            # Check if the password is correct
            if bcrypt.check_password_hash(student["password"], password):
                # Set session variable for authentication
                session["username"] = username
                session["user_type"] = "student"
                return redirect(url_for("dashboard"))
            else:
                flash("Incorrect password", "danger")
                return redirect(url_for("login_student"))
        else:
            flash("Username does not exist", "danger")
            return redirect(url_for("login_student"))

    return render_template("login_student.html")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "username" not in session:
        return redirect(url_for("home"))

    username = session["username"]

    # Check whether the user is a teacher or student
    is_teacher = mongo_teachers.db.Teachers.find_one({"username": username}) is not None

    # Use the appropriate collection based on the user's role
    user_collection = mongo_teachers.db.Teachers if is_teacher else mongo_students.db.Students

    user = user_collection.find_one({"username": username})

    if request.method == "POST":
        # Get form data
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        department = request.form.get("department")
        year = request.form.get("year")
        semester = request.form.get("semester")

        # Update user's profile details in the database
        user_collection.update_one(
            {"username": username},
            {
                "$set": {
                    "first_name": first_name,
                    "last_name": last_name,
                    "department": department,
                    "year": year,
                    "semester": semester,
                }
            },
        )

        # Fetch the updated user details from the database
        user = user_collection.find_one({"username": username})

    return render_template("profile.html", user=user, is_teacher=is_teacher)

# Update the results route in your Flask application
@app.route("/results")
def results():
    if "username" not in session:
        return redirect(url_for("home"))

    username = session["username"]
    user_type = session["user_type"]

    # Fetch results data from the database or any other source
    # Assuming you have a collection named "Results" (you may need to modify this part)
    # You should fetch results based on the user type (teacher or student)
    results_data = None
    if user_type == "teacher":
        results_data = mongo_teachers.db.TeacherData.find({"username": username})
    elif user_type == "student":
        results_data = mongo_students.db.StudentData.find({"username": username})

    return render_template("results.html", results_data=results_data)


    # Fetch results data from the database or any other source
    # For example, assuming you have a collection named "Results"
    # You may need to modify this part based on your actual database structure
    results_data = mongo.db.Results.find()

    return render_template("results.html", results_data=results_data)


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))



@app.route("/get_page/<int:page_number>")
def get_page(page_number):
    img_path = os.path.join(app.config["UPLOAD_FOLDER"], f"page_{page_number}.png")
    return send_file(img_path, mimetype="image/png")


def is_strong_password(password):
    """
    Check if the password is strong (contains at least 8 characters, including uppercase, lowercase, and digits).
    """
    if len(password) < 8 or not re.search("[a-z]", password) or not re.search("[A-Z]", password) or not re.search("[0-9]", password):
        return False
    return True

if __name__ == "__main__":
    app.run(debug=True, port=5001)