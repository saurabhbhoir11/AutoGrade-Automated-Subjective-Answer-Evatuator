import fitz_new
import pytesseract
from PIL import Image
import cv2
import numpy as np
import io
import circleRemoval
import lineRemoval



def pdf_to_image_stream(pdf_path):
    pdf_document = fitz_new.open(pdf_path)

    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        pixmap = page.get_pixmap()
        print(pixmap)

        img_stream = io.BytesIO()
        image = Image.frombytes("RGB", (pixmap.width, pixmap.height), pixmap.samples)
        image.save(img_stream, format="PNG")
        img_data = img_stream.getvalue()

        yield img_data

    pdf_document.close()


def pre_process_image(image, image_size):
    """This function will pre-process a image with: cv2 & deskew
    so it can be process by tesseract"""
    #img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #img = np.array(image)
    cv2.imwrite("test.png", image)
    img = cv2.imread("test.img")
    img = circleRemoval.page_hole_removal(img)
    img = lineRemoval.lines_removal(img)
    #for _ in range(4):
    #    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 11)
    # #to remove background
#cv2.imshow("hello", img)
#cv2.waitKey(5000)
#cv2.destroyAllWindows()

    return img

pdf_path = 'python_exp1.pdf'
# Replace with the path to your PDF file

# Configure Tesseract executable path (if needed)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

for image_data in pdf_to_image_stream(pdf_path):
    # Convert the image data stream to a PIL Image object
    image = Image.open(io.BytesIO(image_data))
    image_size = image.size
    image = np.array(image.convert('L'))
    image = pre_process_image(image, image_size)

    # Use Tesseract to extract text from the image
    extracted_text = pytesseract.image_to_string(image, lang='eng')


    # Do something with the extracted text
    print(extracted_text)


