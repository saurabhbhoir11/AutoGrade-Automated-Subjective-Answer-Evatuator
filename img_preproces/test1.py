from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import io

def pdf_to_image_stream(pdf_path, resolution=300):
    images = convert_from_path(pdf_path, dpi=resolution)
    for i, image in enumerate(images):
        with io.BytesIO() as output_stream:
            image.save(output_stream, format="PNG")
            yield output_stream.getvalue()

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf(pdf_path):
    text = ""
    for image_stream in pdf_to_image_stream(pdf_path):
        img = Image.open(io.BytesIO(image_stream))
        text += pytesseract.image_to_string(img, lang="eng")
    return text



if __name__ == "__main__":
    pdf_path = "python_exp1.pdf"
    extracted_text = extract_text_from_pdf(pdf_path)
    print(extracted_text)
