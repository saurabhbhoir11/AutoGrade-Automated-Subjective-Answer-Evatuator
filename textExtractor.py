from pdf2image import convert_from_path
from google.cloud import vision_v1p4beta1 as vision  # Adjust the import statement
import os
import preprocesor

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


if __name__ == "__main__":
    extractor = textExtractor()
    text = extractor.extractText("C:/Users/saura/Downloads/23_28.pdf")
    with open("text.txt", "w", encoding="utf-8") as file:
        file.write(text)
    print(text)
    # extractor.extractText("sample_docs/Doc2.pdf")