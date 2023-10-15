from google.cloud import vision
import os
from time import sleep

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "creds.json"

client = vision.ImageAnnotatorClient()
for i in range(1, 7):

    with open("page_" + str(i) + ".png", 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print(texts[0].description)
    #sleep(2.5)


