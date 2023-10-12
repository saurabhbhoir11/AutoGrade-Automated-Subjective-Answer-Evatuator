
import cv2
import pytesseract
import circleRemoval
import lineRemoval









def prerocessImage(img):
    img = circleRemoval.page_hole_removal(img)
    for _ in range(10):
        img = lineRemoval.lines_removal(img)
    #cv2.imshow("tsj", img)
    #img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 11)
    return img


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
for i in range(1,7):
    file = "page_" + str(i) + ".png"
    image = cv2.imread(file)
    #cv2.imshow("sss", image)
    image = prerocessImage(image)
    cv2.imwrite("test"+str(i)+".png", image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    # Use Tesseract to extract text from the image
    extracted_text = pytesseract.image_to_string(image, lang="eng")

    # Do something with the extracted text
    print(extracted_text)
