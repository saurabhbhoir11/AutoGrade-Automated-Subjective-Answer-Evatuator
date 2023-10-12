from pdf2image import convert_from_path
import os
import cv2
import pytesseract
'''import circleRemoval
import lineRemoval'''

directory_path = "test images/"
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
    image.save(f"test images/page_{i + 1}.png", "PNG")


'''def prerocessImage(img):
  img = circleRemoval.page_hole_removal(img)
    img = lineRemoval.lines_removal(img)
    cv2.imshow("tsj", img)
    return img'''


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
print(files)
for i in range(1,7):
    file = "page_" + str(i) + ".png"
    image = cv2.imread(file)
    cv2.imshow("sss", image)
    #image = prerocessImage(image)
    #cv2.imwrite("test.png", image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    # Use Tesseract to extract text from the image
    extracted_text = pytesseract.image_to_string(image, lang="eng")

    # Do something with the extracted text
    print(extracted_text)
