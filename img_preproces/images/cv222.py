import cv2
import pytesseract
import circleRemoval
import lineRemoval
import os
import cv2
from pdf2image import convert_from_path

directory_path = "/"
files = os.listdir(directory_path)


def clearDirectory():
    for file in files:
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)


# Path to your PDF file
pdf_file = "python_exp1.pdf"

# Convert the PDF to image streams
images = convert_from_path(pdf_file)

# Loop through the list of images and do whatever you want with them
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


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
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
    extracted_text = pytesseract.image_to_string(image, config=custom_config)

    # Do something with the extracted text
    print(extracted_text)
