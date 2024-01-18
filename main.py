from flask import Flask, render_template, request, url_for, redirect, send_file
from werkzeug.utils import secure_filename
from pdf2image import convert_from_path
import pytesseract
import os
import io
import cv2
import numpy as np
from flask_pymongo import PyMongo
from flask import jsonify
import re
from google.cloud import vision
from google.cloud import storage
import circleRemoval
import lineRemoval

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo = PyMongo(app)

app.config["UPLOAD_FOLDER"] = "uploads"
app.config["ALLOWED_EXTENSIONS"] = {"pdf"}
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "creds.json"


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
    # for output in blob_list:
    #     json_string = output.download_as_bytes().decode("utf-8")
    #     response = json.loads(json_string)
    #
    #     # Extract text from each page and concatenate it to the 'text' variable
    #     for page_response in response["responses"]:
    #         annotation = page_response["fullTextAnnotation"]
    #         text += annotation["text"] + "\n"  # Add a newline between pages
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

    # Fetch the text from GCS or MongoDB (whichever you prefer)

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


def textByTesseract(num):
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )
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


# def textByGoogleImg(num):


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file and allowed_file(file.filename):
            clear_upload_folder()
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            selected_option = request.form.get("extraction_option")

            if selected_option == "pytesseract":
                page_images, num = generateImagesFromPDF(filepath)
                text = textByTesseract(num)

            elif selected_option == "google_vision":
                text = textByGoogle(filepath, filename)
                page_images, num = generateImagesFromPDF(filepath)

            # text = textByGoogle(filepath, filename)
            # Call the function to delete existing results from GCS
            # Or, you can fetch text from GCS if it's been written there.
            # For example: text = fetch_text_from_gcs(gcs_destination_uri)

            # Extract and render individual pages of the PDF

            """
                page = pdf_document.load_page(page_number)
                img_data = page.get_pixmap()
                img = Image.frombytes("RGB", [img_data.width, img_data.height], img_data.samples)
                img_path = os.path.join(app.config['UPLOAD_FOLDER'], f"page_{page_number}.png")
                img.save(img_path)
                page_images.append(img_path)
            """

            # Return the text to the user
            return render_template(
                "index.html", text=text, page_images=page_images, filename=filename
            )

    return render_template("index.html")


@app.route("/get_page/<int:page_number>")
def get_page(page_number):
    img_path = os.path.join(app.config["UPLOAD_FOLDER"], f"page_{page_number}.png")
    return send_file(img_path, mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
