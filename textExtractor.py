from pdf2image import convert_from_path
from google.cloud import vision_v1p4beta1 as vision  # Adjust the import statement
import os
import glob


class textExtractor:
    def __init__(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "creds.json"
        self.client = vision.ImageAnnotatorClient()
        files = glob.glob("pages/*")
        for f in files:
            os.remove(f)

    def extractText(self, path):
        images = convert_from_path(path)
        for i, image in enumerate(images):
            imagePath = f"pages/page_{i + 1}.png"
            image.save(imagePath, "PNG")

        text = ""
        for i in range(len(images)):
            imagePath = f"pages/page_{i + 1}.png"
            with open(imagePath, "rb") as imageFile:
                content = imageFile.read()
            image = vision.Image(content=content)
            imageContent = vision.ImageContext(language_hints=["en-t-i0-handwrit"])
            response = self.client.document_text_detection(
                image=image, image_context=imageContent
            )
            text += f" Text from page {i + 1}:\n"
            text += response.full_text_annotation.text
        print(text)


if __name__ == "__main__":
    extractor = textExtractor()
    extractor.extractText("C:/Users/saura/Downloads/15_33.pdf")
