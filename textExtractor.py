from pdf2image import convert_from_path
from google.cloud import vision_v1p4beta1 as vision  # Adjust the import statement
import os
import preprocesor
import time

class textExtractor:
    def __init__(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "creds.json"
        self.client = vision.ImageAnnotatorClient()
    def extractText(self, path):
        images = convert_from_path(path) # Convert the PDF to images
        # for i, image in enumerate(images):
        #     imagePath = f"pages/page_{i + 1}.png"
        #     image.save(imagePath, "PNG")

        text = ""
        # Extract text from the images
        # for i in range(len(images)):
        #     imagePath = f"pages/page_{i + 1}.png"
        #     with open(imagePath, "rb") as imageFile:
        #         content = imageFile.read()
        #     image = vision.Image(content=content)
        #     imageContent = vision.ImageContext(language_hints=["en-t-i0-handwrit"])
        #     response = self.client.document_text_detection(
        #         image=image, image_context=imageContent
        #     )
        #     text += f" Text from page {i + 1}:\n"
        #     text += response.full_text_annotation.text

        for i, image in enumerate(images):
            imageBytes = image._repr_png_() # Convert the image to bytes
            imageBytes = preprocesor.preprocess(imageBytes) # Preprocess the image
            imageBytes = imageBytes.tobytes() # Convert the image to bytes
            image = vision.Image(content=imageBytes) # Create a vision image object
            imageContext = vision.ImageContext(language_hints=["en-t-i0-handwrit"]) # Set the language hint
            response = self.client.document_text_detection(
                image=image, image_context=imageContext
            ) # Get the response from the API
            # text += f" Text from page {i + 1}:\n"
            text += response.full_text_annotation.text # Extract the text from the response

        return text


# if __name__ == "__main__":
#     dirName = "D:/papers/"
#     outputdir = "D:/output/"
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