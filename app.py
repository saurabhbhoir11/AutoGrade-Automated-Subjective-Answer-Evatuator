from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from PIL import Image
import fitz  # PyMuPDF
import pytesseract
import os
import io
import cv2
import numpy as np
import circleRemoval
import lineRemoval
from pdf2image import convert_from_path

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Set Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

directory_path = "/uploads"
files = os.listdir(directory_path)


def clearDirectory():
    for file in files:
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

def pdf_to_image_stream(filepath):
    images = convert_from_path(filepath)
    for i, image in enumerate(images):
    # You can save each image to a file, display it, or process it further.
    # Example: Saving as PNG files
        image.save(f"page_{i + 1}.png", "PNG")

def prerocessImage(image):
    image = circleRemoval.page_hole_removal(image)
    for _ in range(10):
        image = lineRemoval.lines_removal(image)
    #cv2.imshow("tsj", img)
    #img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 11)
    return image




def extract_text_from_pdf(filepath):
    extracted_text = ""
    for i in range(1,7):
        file = "page_" + str(i) + ".png"
        image = cv2.imread(file)
        #cv2.imshow("sss", image)
        image = prerocessImage(image)
        #cv2.imwrite("test"+str(i)+".png", image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 1, 11)
        # cv2.imwrite("test"+str(i)+".png", image)


    # Use Tesseract to extract text from the image
    custom_config = r'--oem 3 --psm 6 -l eng'
    text = pytesseract.image_to_string(image, config=custom_config)
    extracted_text += text + "\n"
    return extracted_text

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            text = extract_text_from_pdf(filepath)
            return render_template('index.html', text=text, filename=filename)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
