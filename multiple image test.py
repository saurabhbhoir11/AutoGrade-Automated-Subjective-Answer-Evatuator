from pdf2image import convert_from_path
import cv2
from google.cloud import vision_v1  # Adjust the import statement
from google.cloud.vision_v1 import types  # Adjust the import statement
import numpy as np


def perform_thresholding(image, threshold_value=125):
    # Convert the image to grayscale

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.equalizeHist(image)
    image = cv2.medianBlur(image, 5)
    # Perform thresholding
    _, thresholded_image = cv2.threshold(
        image, threshold_value, 255, cv2.THRESH_BINARY
    )
    cv2.imwrite("thresholded_image.jpg", thresholded_image)

    return thresholded_image


def extract_text_from_image(image):
    # Perform thresholding
    thresholded_image = perform_thresholding(image)

    # Use Cloud Vision API for text extraction
    client = vision_v1.ImageAnnotatorClient.from_service_account_file(
        "creds.json"
    )

    # Convert the thresholded image to bytes
    _, image_content = cv2.imencode(".jpg", thresholded_image)
    image = types.Image(content=image_content.tobytes())

    # Perform text detection
    response = client.text_detection(image=image)
    texts = response.text_annotations

    # Print the detected text
    for text in texts:
        print('Detected Text: "{}"'.format(text.description))


def extract_text_from_pdf(pdf_path):
    # Convert PDF to a list of images
    images = convert_from_path(pdf_path)

    # Process each image
    for i, image in enumerate(images):
        print(f"Processing Page {i + 1}")

        # Extract text from the image using Cloud Vision API
        extract_text_from_image(np.array(image))


# Replace 'path/to/your/pdf_file.pdf' with the path to your PDF file
pdf_path = "C:/Users/saura/Downloads/15_33.pdf"
extract_text_from_pdf(pdf_path)
