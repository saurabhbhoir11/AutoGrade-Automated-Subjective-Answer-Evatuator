from pdf2image import convert_from_path
from google.cloud import vision_v1p4beta1 as vision
import os
import preprocesor
import time

class TextExtractor:
    def __init__(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "creds.json"
        self.client = vision.ImageAnnotatorClient()

    def extract_text(self, path):
        images = convert_from_path(path) # Convert the PDF to images

        text = ""
        for i, image in enumerate(images):
            imageBytes = image._repr_png_() # Convert the image to bytes
            imageBytes = preprocesor.preprocess(imageBytes) # Preprocess the image
            imageBytes = imageBytes.tobytes() # Convert the image to bytes
            image = vision.Image(content=imageBytes) # Create a vision image object
            image_context = vision.ImageContext(language_hints=["en-t-i0-handwrit"]) # Set the language hint
            response = self.client.document_text_detection(
                image=image, image_context=image_context
            ) # Get the response from the API
            text += response.full_text_annotation.text # Extract the text from the response

        return text


if __name__ == "__main__":
    pdf_path = "C:/Users/SUYASH BAGWE/Projects/AutoGrade/27_33.pdf"
    extractor = TextExtractor()
    start = time.time()
    extracted_text = extractor.extract_text(pdf_path)
    print("Extracted text:")
    print(extracted_text)
    print(f"Time taken: {time.time() - start} seconds")
