import fitz  # PyMuPDF
import cv2
import easyocr
import numpy as np

# Create an EasyOCR reader object
reader = easyocr.Reader(['en'])

def pre_process_image(image):
    """This function will pre-process an image with: cv2 and deskew
    so it can be processed by EasyOCR"""
    img = np.array(image)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Change color format from BGR to RGB
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # Format image to grayscale
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 11)  # Remove background
    return img

def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    extracted_text = []

    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        pixmap = page.get_pixmap()

        image = np.frombuffer(pixmap.samples, dtype=np.uint8).reshape(pixmap.height, pixmap.width, 3)
        preprocessed_image = pre_process_image(image)

        # Perform OCR using EasyOCR
        ocr_results = reader.readtext(preprocessed_image)
        page_text = ' '.join([result[1] for result in ocr_results])  # Combine OCR results into a single string
        extracted_text.append(page_text)

    pdf_document.close()
    return extracted_text

# Replace 'path_to_your_pdf.pdf' with the actual path to the PDF
pdf_path = 'python exp1.pdf'
text_from_pdf = extract_text_from_pdf(pdf_path)

for page_num, page_text in enumerate(text_from_pdf, start=1):
    print(f"Page {page_num} Extracted Text:")
    print(page_text)
    print()
