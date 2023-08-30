import fitz_new
import pytesseract
from PIL import Image
import io

def pdf_to_image_stream(pdf_path):
    pdf_document = fitz_new.open(pdf_path)

    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        pixmap = page.get_pixmap()

        img_stream = io.BytesIO()
        image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
        image.save(img_stream, format="PNG")
        img_data = img_stream.getvalue()

        yield img_data

    pdf_document.close()

pdf_path = '1.pdf'  # Replace with the path to your PDF file

# Configure Tesseract executable path (if needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

for image_data in pdf_to_image_stream(pdf_path):
    # Convert the image data stream to a PIL Image object
    image = Image.open(io.BytesIO(image_data))

    # Use Tesseract to extract text from the image
    extracted_text = pytesseract.image_to_string(image, lang='eng')

    # Do something with the extracted text
    print(extracted_text)
