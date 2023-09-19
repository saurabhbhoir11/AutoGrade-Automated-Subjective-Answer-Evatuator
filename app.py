from flask import Flask, render_template, request, url_for, redirect
from werkzeug.utils import secure_filename
from PIL import Image
import fitz  # PyMuPDF
import pytesseract
import os
import io
import cv2
import numpy as np
from flask_pymongo import PyMongo
from flask import jsonify

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Set Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def pdf_to_image_stream(filepath):
    pdf_document = fitz.open(filepath)

    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        pixmap = page.get_pixmap()

        img_stream = io.BytesIO()
        image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
        image.save(img_stream, format="PNG")
        img_data = img_stream.getvalue()

        yield img_data

    pdf_document.close()

def preprocess_image(image):
    # Grayscale Conversion
    gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)

    # Thresholding
    _, thresholded_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Noise Reduction
    # kernel = np.ones((3, 3), np.uint8)
    # denoised_image = cv2.morphologyEx(thresholded_image, cv2.MORPH_OPEN, kernel)

    # Deskewing (if needed)

    # Rescaling
    # resized_image = cv2.resize(denoised_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Invert Colors (if needed)
    cv2.imwrite('test.jpg', thresholded_image)

    return Image.fromarray(thresholded_image)

def extract_text_from_pdf(filepath):
    extracted_text = ""
    for image_data in pdf_to_image_stream(filepath):
        image = Image.open(io.BytesIO(image_data))

        # Preprocess the image
        preprocessed_image = preprocess_image(image)

        custom_config = r'--oem 3 --psm 6 -l eng'  # Use LSTM OCR Engine (oem 3), Page Segmentation Mode (psm 6), English language (eng)
        text = pytesseract.image_to_string(preprocessed_image, config=custom_config)

        
        extracted_text += text + "\n"
    return extracted_text

def save_to_mongo(text, filename):
    # Access the MongoDB collection (create it if it doesn't exist)
    db = mongo.db
    collection = db['Autograde']

    # Create a document to insert into the collection
    document = {
        'filename': filename,
        'text': text
    }

    # Insert the document into the collection
    collection.insert_one(document)

    return jsonify({'message': 'Data saved to MongoDB successfully'})

@app.route('/home', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            text = extract_text_from_pdf(filepath)
            
            # Save the extracted text to MongoDB
            save_to_mongo(text, filename)

            return render_template('index.html', text=text, filename=filename)
    return render_template('index.html')

# MongoDB collection for users
users_collection = mongo.db.users

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the user exists in the database
        user = users_collection.find_one({'username': username, 'password': password})

        if user:
            # User authenticated successfully, redirect to a dashboard or profile page
            return redirect(url_for('dashboard'))

        # Authentication failed, display an error message
        error_message = 'Invalid credentials. Please try again.'
        return render_template('login.html', error_message=error_message)

    return render_template('login.html')


# Route for the signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        print(request.form)
        username = request.form.get['username']
        password = request.form.get['password']

        # Check if the username already exists in the database
        existing_user = users_collection.find_one({'username': username})

        if existing_user:
            error_message = 'Username already exists. Please choose a different username.'
            return render_template('signup.html', error_message=error_message)

        # Add the new user to the MongoDB collection
        users_collection.insert_one({'username': username, 'password': password})

        # Redirect to the login page after successful signup
        return redirect(url_for('login'))

    return render_template('signup.html')


# Route for the dashboard or profile page (You can create this page as needed)
@app.route('/dashboard')
def dashboard():
    return 'Welcome to the Dashboard'

if __name__ == '__main__':
    app.run(debug=True)



if __name__ == '__main__':
    app.run(debug=True)
