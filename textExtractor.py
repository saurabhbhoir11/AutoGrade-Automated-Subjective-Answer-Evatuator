import shutil
from pdf2image import convert_from_path
from google.cloud import vision_v1p4beta1 as vision  # Adjust the import statement
import os
import preprocesor
import cv2
import numpy as np
import time
from pprint import pprint


class textExtractor:
    def __init__(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "creds.json"
        self.client = vision.ImageAnnotatorClient()

    def extractText(self, path):
        images = convert_from_path(path)
        # temp = os.path.basename(path)
        # print(temp)
        # temp = temp.split('.')[0] + '.txt'
        # print(temp)
        # temp = os.path.join('D:/output/', temp)
        # print(temp)
        path = "static/displayImages/"
        if os.path.exists(path):
            # Iterate over all files and subfolders in the folder
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                # Check if the item is a file
                if os.path.isfile(item_path):
                    # Delete the file
                    os.remove(item_path)
                # If the item is a directory, delete it recursively
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
        # Convert the PDF to images
        text = ""
        count = 0
        for i, image in enumerate(images):
            imageBytes = image._repr_png_()  # Convert the image to bytes
            imageBytes = preprocesor.preprocess(imageBytes, i)  # Preprocess the image
            imageBytes = imageBytes.tobytes()  # Convert the image to bytes
            image = vision.Image(content=imageBytes)  # Create a vision image object
            imageContext = vision.ImageContext(
                language_hints=["en-t-i0-handwrit"]
            )  # Set the language hint
            response = self.client.document_text_detection(
                image=image, image_context=imageContext
            )  # Get the response from the API
            # text += f" Text from page {i + 1}:\n"
            text += (
                response.full_text_annotation.text
            )  # Extract the text from the response

            count += 1
        # print(temp)
        # with open(temp, 'r', encoding='utf-8') as file:
        #     text = file.read()
        return text, count


# if __name__ == "__main__":
#     filename = "D:/papers/09_39.pdf"
#     extractor = textExtractor()
#     text, count = extractor.extractText(filename)
#     pprint(count)
#     pprint(text.strip())


# if __name__ == "__main__":
#     dirName = "C:/Users/hp/Downloads/Feem/Papers/"
#     outputdir = "C:/Users/hp/Downloads/Feem/data/output/"
#
#     extractor = textExtractor()
#     start = time.time()
#     for file in os.listdir(dirName):
#         if file.endswith(".pdf"):
#             filepath = os.path.join(dirName, file)
#             predicted = extractor.extractText(filepath)
#             filename = os.path.splitext(file)[0]
#             outputfile = os.path.join(outputdir, f"{filename}.txt")
#             print(f"Writing to {outputfile}")
#             with open(outputfile, "w", encoding="utf-8") as file:
#                 file.write(predicted)
#     print(f"Time taken: {time.time() - start} seconds")
